#!/usr/bin/env python3
"""
Build script for Multi-omics and (bio)Imaging Metadata (MIM).
Parses modular LinkML YAML schemas across schemas/foundation and schemas/profiles,
resolves mixins and inheritance (is_a), and outputs model.json and details.json.
"""

import os
import glob
import json
import yaml


def load_all_schemas(schema_root="schemas"):
    """Recursively scan and load all active LinkML YAML schema files under schema_root."""
    schemas = {}
    yaml_files = glob.glob(os.path.join(schema_root, "**/*.yaml"), recursive=True)
    
    for filepath in yaml_files:
        # Ignore legacy/archived version files to prevent syntax error noise
        if "older_versions" in filepath or "to_be_checked" in filepath:
            continue
            
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
                if data and isinstance(data, dict):
                    schema_id = data.get("id") or os.path.basename(filepath)
                    schemas[schema_id] = data
        except Exception as e:
            print(f"[Schema Parser] Error loading {filepath}: {e}")
            
    return schemas


def consolidate_model(schemas):
    """Parse LinkML schemas, resolve class inheritance & mixins, and extract field details."""
    classes = {}
    enums = {}
    total_fields_count = 0

    # Pass 1: Extract all raw class definitions and enumerations
    for schema_id, schema in schemas.items():
        module_name = schema.get("annotations", {}).get("module_name", "general")
        profile_name = schema.get("annotations", {}).get("profile", "foundation")

        # Parse Enumerations
        for enum_name, enum_def in schema.get("enums", {}).items():
            p_vals = []
            if isinstance(enum_def, dict) and "permissible_values" in enum_def:
                pv_data = enum_def["permissible_values"]
                if isinstance(pv_data, dict):
                    p_vals = list(pv_data.keys())
                elif isinstance(pv_data, list):
                    p_vals = pv_data
            enums[enum_name] = {
                "name": enum_name,
                "permissible_values": p_vals,
                "description": enum_def.get("description", "") if isinstance(enum_def, dict) else ""
            }

        # Parse Classes
        for cls_name, cls_def in schema.get("classes", {}).items():
            if not isinstance(cls_def, dict):
                continue
            classes[cls_name] = {
                "name": cls_name,
                "description": cls_def.get("description", ""),
                "class_uri": cls_def.get("class_uri", ""),
                "is_a": cls_def.get("is_a", None),
                "mixins": cls_def.get("mixins", []),
                "abstract": cls_def.get("abstract", False),
                "module": module_name,
                "profile": profile_name,
                "attributes": cls_def.get("attributes", {}),
                "slot_usage": cls_def.get("slot_usage", {})
            }

    # Recursive attribute resolution function (is_a + mixins)
    def get_all_attributes(cls_name, visited=None):
        if visited is None:
            visited = set()
        if cls_name in visited or cls_name not in classes:
            return {}
        visited.add(cls_name)

        cls = classes[cls_name]
        resolved_attrs = {}

        # 1. Inherit from parent class (is_a)
        if cls.get("is_a"):
            resolved_attrs.update(get_all_attributes(cls["is_a"], visited.copy()))

        # 2. Inherit from mixins
        for mixin in cls.get("mixins", []):
            resolved_attrs.update(get_all_attributes(mixin, visited.copy()))

        # 3. Apply class's own declared attributes
        for attr_name, attr_def in cls.get("attributes", {}).items():
            if isinstance(attr_def, dict):
                attr_data = dict(attr_def)
                attr_data["declared_in"] = cls_name
                resolved_attrs[attr_name] = attr_data

        return resolved_attrs

    model_tree = []
    details_map = {}

    # Pass 2: Build tree structure and full details dictionary
    for cls_name, cls in sorted(classes.items()):
        all_attrs = get_all_attributes(cls_name)
        fields_list = []

        for attr_name, attr_info in sorted(all_attrs.items()):
            field_path = f"{cls_name}.{attr_name}"
            attr_range = attr_info.get("range", "string")
            is_enum = attr_range in enums
            total_fields_count += 1

            fields_list.append({
                "path": field_path,
                "name": attr_name,
                "range": attr_range,
                "required": attr_info.get("required", False),
                "multivalued": attr_info.get("multivalued", False),
                "inlined": attr_info.get("inlined", False),
                "declared_in": attr_info.get("declared_in", cls_name),
                "is_enum": is_enum
            })

            details_map[field_path] = {
                "class": cls_name,
                "attribute": attr_name,
                "description": attr_info.get("description", ""),
                "slot_uri": attr_info.get("slot_uri", ""),
                "range": attr_range,
                "required": attr_info.get("required", False),
                "multivalued": attr_info.get("multivalued", False),
                "inlined": attr_info.get("inlined", False),
                "pattern": attr_info.get("pattern", None),
                "declared_in": attr_info.get("declared_in", cls_name),
                "is_enum": is_enum,
                "enum_values": enums[attr_range]["permissible_values"] if is_enum else []
            }

        model_tree.append({
            "class": cls_name,
            "description": cls["description"],
            "module": cls["module"],
            "profile": cls["profile"],
            "abstract": cls["abstract"],
            "is_a": cls["is_a"],
            "mixins": cls["mixins"],
            "fields": fields_list
        })

    summary_stats = {
        "classes_count": len(classes),
        "enums_count": len(enums),
        "total_fields": total_fields_count
    }

    return {"summary": summary_stats, "classes": model_tree, "enums": enums}, details_map


def build():
    """Build task outputting model.json and details.json to docs/data/."""
    os.makedirs("docs/data", exist_ok=True)
    schemas = load_all_schemas("schemas")
    model_data, details_data = consolidate_model(schemas)

    with open("docs/data/model.json", "w", encoding="utf-8") as f:
        json.dump(model_data, f, indent=2)

    with open("docs/data/details.json", "w", encoding="utf-8") as f:
        json.dump(details_data, f, indent=2)

    print(f"[Schema Parser] Built docs/data/model.json ({model_data['summary']['classes_count']} classes, "
          f"{model_data['summary']['enums_count']} enums) & details.json.")


def on_config(config, **kwargs):
    """MkDocs hook entry point called during build/serve."""
    build()
    return config


if __name__ == "__main__":
    build()