CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE address(
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    country VARCHAR(255) NOT NULL,
    city VARCHAR(255) NOT NULL,
    street VARCHAR(255) NOT NULL
);

CREATE TABLE client(
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    client_name VARCHAR(255) NOT NULL,
    client_surname VARCHAR(255) NOT NULL,
    birthday DATE NOT NULL,
    gender CHAR(1) CHECK (gender IN ('M', 'F')),
    registration_date TIMESTAMP NOT NULL,
    address_id UUID REFERENCES address(id)
);

CREATE TABLE category(
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL
);

CREATE TABLE images(
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    image BYTEA NOT NULL
);

CREATE TABLE supplier(
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    address_id UUID REFERENCES address(id),
    phone_number VARCHAR(20)
);

CREATE TABLE product(
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    category_id INTEGER REFERENCES category(id),
    price DECIMAL(10, 2) NOT NULL,
    available_stock INTEGER NOT NULL,
    last_update_date TIMESTAMP NOT NULL,
    supplier_id UUID REFERENCES supplier(id),
    image_id UUID REFERENCES images(id)
);

