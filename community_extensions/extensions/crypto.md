---
layout: community_extension_doc
title: crypto
excerpt: |
  DuckDB Community Extensions
  Cryptographic hash functions and HMAC

docs:
  extended_description: "`crypto` provides two functions:\n\n- `crypto_hash` applies\
    \ cryptographically secure hash functions\nand returns the result as a hex encoded\
    \ value.\n\n- `crypto_hmac` calculates the HMAC using a secret key and a\nspecific\
    \ hash function.\n\nThe supported hash functions are:\n  - `blake2b-512`\n  -\
    \ `keccak224`\n  - `keccak256`\n  - `keccak384`\n  - `keccak512`\n  - `md4`\n\
    \  - `md5`\n  - `sha1`\n  - `sha2-224`\n  - `sha2-256`\n  - `sha2-384`\n  - `sha2-512`\n\
    \  - `sha3-224`\n  - `sha3-256`\n  - `sha3-384`\n  - `sha3-512`"
  hello_world: '-- Calculate the MD5 hash value of ''abcdef''

    SELECT crypto_hash(''md5'', ''abcdef'');

    ┌──────────────────────────────────┐

    │   crypto_hash(''md5'', ''abcdef'')   │

    │             varchar              │

    ├──────────────────────────────────┤

    │ e80b5017098950fc58aad83c8c14978e │

    └──────────────────────────────────┘


    -- Calculate a HMAC

    SELECT crypto_hmac(''sha2-256'', ''secret key'', ''secret message'');

    ┌──────────────────────────────────────────────────────────────────┐

    │     crypto_hmac(''sha2-256'', ''secret key'', ''secret message'')      │

    │                             varchar                              │

    ├──────────────────────────────────────────────────────────────────┤

    │ 2df792e08cefdc0ea9900c67c93cbe66b98231b829a5dccd3857a03baac35963 │

    └──────────────────────────────────────────────────────────────────┘

    '
extension:
  build: cmake
  description: Cryptographic hash functions and HMAC
  excluded_platforms: windows_amd64_rtools;windows_amd64
  language: C++
  license: MIT
  maintainers:
  - rustyconover
  name: crypto
  requires_toolchains: rust
  version: 1.0.0
repo:
  github: rustyconover/duckdb-crypto-extension
  ref: c8a64d43bafa559f48dd55730813475eb58c4916

extension_star_count: 9

---

### Installing and Loading
```sql
INSTALL {{ page.extension.name }} FROM community;
LOAD {{ page.extension.name }};
```

{% if page.docs.hello_world %}
### Example
```sql
{{ page.docs.hello_world }}```
{% endif %}

{% if page.docs.extended_description %}
### About {{ page.extension.name }}
{{ page.docs.extended_description }}
{% endif %}

### Added Functions

<div class="extension_functions_table"></div>

| function_name | function_type |                                                   description                                                    | comment |                             example                             |
|---------------|---------------|------------------------------------------------------------------------------------------------------------------|---------|-----------------------------------------------------------------|
| crypto_hash   | scalar        | Apply a cryptographic hash function specified as the first argument to the data supplied as the second argument. |         | SELECT crypto_hash('md5', 'test');                              |
| crypto_hmac   | scalar        | Calculate a HMAC value                                                                                           |         | SELECT crypto_hmac('sha2-256', 'secret key', 'secret message'); |



---
