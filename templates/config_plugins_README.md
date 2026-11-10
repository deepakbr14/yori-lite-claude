Plugin configuration in Google Drive

This visible My Drive folder contains private configuration pointers under normal Google permissions. It is a proposed convention, not an official Google or Anthropic standard. Do not share it by default or store secrets here.

Yori Lite uses `yori_2d970fa0-89e4-451e-802b-9f836f99d9e1.json`. The description contains schema_version 1 JSON with plugin_id `yori_2d970fa0-89e4-451e-802b-9f836f99d9e1` and one active_cortex (label, google_drive_folder_id). The file contents can be empty. Older configurations may still contain the identical JSON in contents; 0.2 can read them without editing contents. Invalid or conflicting configuration stops setup rather than choosing another folder.

Each user owns their own config. The fixed plugin UUID is shared across installations, not a user identifier. Different users can choose the same authorized Cortex. Other plugins' files remain untouched. Duplicate registry/config files require explicit resolution. Current version supports one Cortex with no switching.
