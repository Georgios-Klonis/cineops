# Workflow

1. Install the DBML CLI if needed:
   ```sh
   npm install -g @dbml/cli
   ```

2. Model the schema in `cineops.dbml`.

3. Compile the DBML to a PostgreSQL DDL script:
   ```sh
   dbml2sql --postgres \
      backend/db/schema/cineops.dbml \
      -o backend/db/schema/cineops.sql
   ```
