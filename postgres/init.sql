-- Create test database
CREATE DATABASE testdb;

-- Connect to test database
\c testdb;

-- Create a sample schema for multidimensional data
CREATE TABLE multidim_points (
    id SERIAL PRIMARY KEY,
    point cube,
    metadata JSONB
);

-- Create an index for efficient querying
CREATE INDEX idx_multidim_points ON multidim_points USING gist (point);

-- Insert some sample data
INSERT INTO multidim_points (point, metadata) VALUES 
    ('(0,0,0)', '{"description": "Origin point"}'),
    ('(1,2,3)', '{"description": "Sample point 1"}'),
    ('(4,5,6)', '{"description": "Sample point 2"}');

-- Create a user for application access
CREATE USER testuser WITH PASSWORD 'testpassword';
GRANT ALL PRIVILEGES ON DATABASE testdb TO testuser;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO testuser;