# Database Workflow

1. Import raw TMDB data via Kaggle and download it into `seeds/raw/`.
2. Clean and enrich the dataset in `seeds/explore_tmdb.ipynb`, then export the processed CSVs (movies, genres) into `seeds/processed/`.
3. Model the relational schema in `schema/cineops.dbml` and compile it to `schema/cineops.sql` using the DBML CLI:

   ```sh
   npm install -g @dbml/cli
   dbml2sql --postgres \
     backend/db/schema/cineops.dbml \
     -o backend/db/schema/cineops.sql
   ```

4. Apply Alembic migrations to create the schema in PostgreSQL:

   ```sh
   docker run \
     --name cineops-postgres \
     -e POSTGRES_USER=cineops \
     -e POSTGRES_PASSWORD=cineops \
     -e POSTGRES_DB=cineops_dev \
     -p 5432:5432 \
     -d postgres:16
   ```

   ```sh
   pip install alembic
   pip install python-dotenv
   pip install psycopg2-binary
   alembic init backend/db/migrations
   alembic upgrade head
   ```
