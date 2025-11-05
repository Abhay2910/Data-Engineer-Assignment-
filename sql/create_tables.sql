-- Drop tables if exist
DROP TABLE IF EXISTS valuations;
DROP TABLE IF EXISTS rehab_estimates;
DROP TABLE IF EXISTS hoa;
DROP TABLE IF EXISTS properties;

-- Create main properties table
CREATE TABLE properties (
    property_id INT PRIMARY KEY,
    address VARCHAR(255),
    city VARCHAR(100),
    state VARCHAR(50),
    zip_code VARCHAR(20),
    property_type VARCHAR(50),
    bedrooms INT,
    bathrooms DECIMAL(3,1),
    area_sqft INT,
    price DECIMAL(12,2)
);

-- Create HOA table
CREATE TABLE hoa (
    hoa_id INT PRIMARY KEY AUTO_INCREMENT,
    property_id INT,
    hoa_fee DECIMAL(10,2),
    FOREIGN KEY (property_id) REFERENCES properties(property_id)
);

-- Create Rehab Estimates table
CREATE TABLE rehab_estimates (
    rehab_id INT PRIMARY KEY AUTO_INCREMENT,
    property_id INT,
    estimated_cost DECIMAL(12,2),
    last_updated DATE,
    FOREIGN KEY (property_id) REFERENCES properties(property_id)
);

-- Create Valuations table
CREATE TABLE valuations (
    valuation_id INT PRIMARY KEY AUTO_INCREMENT,
    property_id INT,
    valuation_amount DECIMAL(12,2),
    valuation_date DATE,
    FOREIGN KEY (property_id) REFERENCES properties(property_id)
);
