CREATE TABLE if not exists AdminUser (
  username varchar(250) NOT NULL,
  password varchar(250) NOT NULL,
  first_name varchar(250) NOT NULL,
  last_name varchar(250) NOT NULL,
  PRIMARY KEY (username)
);

CREATE TABLE if not exists Manager (
  username varchar(250) NOT NULL,
  password varchar(250) NOT NULL,
  first_name varchar(250) NOT NULL,
  last_name varchar(250) NOT NULL,
  PRIMARY KEY (username)
);

CREATE TABLE if not exists SalesPeople (
  username varchar(250) NOT NULL,
  password varchar(250) NOT NULL,
  first_name varchar(250) NOT NULL,
  last_name varchar(250) NOT NULL,
  PRIMARY KEY (username)
);

CREATE TABLE if not exists InventoryClerk (
  username varchar(250) NOT NULL,
  password varchar(250) NOT NULL,
  first_name varchar(250) NOT NULL,
  last_name varchar(250) NOT NULL,
  PRIMARY KEY (username)
);

CREATE TABLE if not exists Vehicle (
  vin varchar(250) NOT NULL,
  vehicle_type varchar(250) NOT NULL,
  manufacturer_name varchar(250) NOT NULL,
  fuel_type varchar(250) NOT NULL,
  model_name varchar(250) NOT NULL,
  model_year numeric(4,0) NOT NULL,
  description varchar(2000) DEFAULT NULL, 
  mileage float NOT NULL,
  PRIMARY KEY (vin)
);

CREATE TABLE if not exists VehicleType (
  vehicle_type varchar(250) NOT NULL,
  PRIMARY KEY (vehicle_type)
);

CREATE TABLE if not exists VehicleManufacturer (
  manufacturer_name varchar(250) NOT NULL,
  PRIMARY KEY (manufacturer_name)
);

CREATE TABLE if not exists VehicleColor (
  color varchar(250) NOT NULL,
  vin varchar(250) NOT NULL,
  PRIMARY KEY (color,vin)
);

CREATE TABLE if not exists Customer (
  customer_id  uuid NOT NULL,
  street varchar(250) NOT NULL,
  city varchar(250) NOT NULL,
  state varchar(250) NOT NULL,
  postal_code varchar(250) NOT NULL,
  phone_number varchar(250) NOT NULL,
  email varchar(250),
  PRIMARY KEY(customer_id)  
);

CREATE TABLE if not exists CustomerIndividual (
  drivers_license_number varchar(250) NOT NULL,
  customer_id varchar(250) NOT NULL,
  first_name varchar(250) NOT NULL,
  last_name varchar(250) NOT NULL,
  PRIMARY KEY(drivers_license_number)
);

CREATE TABLE if not exists CustomerBusiness (
  tax_id_number varchar(250) NOT NULL,
  customer_id varchar(250) NOT NULL,
  contact_name varchar(250) NOT NULL,
  title varchar(250) NOT NULL,
  PRIMARY KEY(tax_id_number)
);

CREATE TABLE if not exists Buy (
  customer_id varchar(250) NOT NULL,
  vin varchar(250) NOT NULL,
  username varchar(250) NOT NULL,
  sale_date date NOT NULL,
  sale_price float NOT NULL,
  PRIMARY KEY(customer_id,vin,username)
);

CREATE TABLE if not exists Sell (
  customer_id varchar(250) NOT NULL,
  vin varchar(250) NOT NULL,
  username varchar(250) NOT NULL,
  purchase_price float NOT NULL,
  purchase_date date NOT NULL,
  vehicle_condition varchar(250) NOT NULL,
  PRIMARY KEY(customer_id,vin,username)
);

CREATE TABLE if not exists PartOrder (
  purchase_order_number varchar(250) UNIQUE NOT NULL,
  vin varchar(250) NOT NULL,
  part_vendor_name varchar(250) NOT NULL,
  username varchar(250) NOT NULL,
  total_cost float NOT NULL,
  PRIMARY KEY(purchase_order_number,vin)
);

CREATE TABLE if not exists PartVendor(
  name varchar(250) NOT NULL,
  phone_number varchar(250) NOT NULL,
  street varchar(250) NOT NULL,
  city varchar(250) NOT NULL,
  state varchar(250) NOT NULL,
  postal_code varchar(250) NOT NULL,
  PRIMARY KEY(name)
);

CREATE TABLE if not exists Part (
  part_number varchar(250) NOT NULL,
  purchase_order_number varchar(250) NOT NULL,
  description varchar(250) DEFAULT NULL,
  status varchar(250) NOT NULL,
  cost float NOT NULL,
  quantity integer NOT NULL,
  PRIMARY KEY(part_number, purchase_order_number)
);

ALTER TABLE Part
  ADD CONSTRAINT fk_Part_purchaseOrderNumber_PartOrder_purchaseOrderNumber FOREIGN KEY (purchase_order_number) REFERENCES PartOrder(purchase_order_number);
  
ALTER TABLE PartOrder
  ADD CONSTRAINT fk_PartOrder_partVendorName_PartVendor_name FOREIGN KEY (part_vendor_name) REFERENCES PartVendor(name),
  ADD CONSTRAINT fk_PartOrder_username_InventoryClerk_username FOREIGN KEY(username) REFERENCES InventoryClerk(username),
  ADD CONSTRAINT fk_PartOrder_vin_Vehicle_vin FOREIGN KEY (vin) REFERENCES Vehicle(vin);
  
ALTER TABLE Sell
  ADD CONSTRAINT fk_Sell_customerId_Customer_customerId FOREIGN KEY (customer_id) REFERENCES Customer(customer_id),
  ADD CONSTRAINT fk_Sell_vin_Vehicle_vin FOREIGN KEY (vin) REFERENCES Vehicle(vin),
  ADD CONSTRAINT fk_Sell_username_InventoryClerk_username FOREIGN KEY (username) REFERENCES InventoryClerk(username);
  
ALTER TABLE Buy
  ADD CONSTRAINT fk_Buy_customerId_Customer_customerId FOREIGN KEY (customer_id) REFERENCES Customer(customer_id),
  ADD CONSTRAINT fk_Buy_vin_Vehicle_vin FOREIGN KEY (vin) REFERENCES Vehicle(vin),
  ADD CONSTRAINT fk_Buy_username_SalesPeople_username FOREIGN KEY (username) REFERENCES SalesPeople (username);
  
ALTER TABLE CustomerBusiness
  ADD CONSTRAINT fk_CustomerBusiness_customerId_Customer_customerId FOREIGN KEY (customer_id) REFERENCES Customer(customer_id);
  
ALTER TABLE CustomerIndividual
  ADD CONSTRAINT fk_CustomerIndividual_customerId_Customer_customerId FOREIGN KEY (customer_id) REFERENCES Customer(customer_id);
  
ALTER TABLE VehicleColor
  ADD CONSTRAINT fk_VehicleColor_vin_Vehicle_vin FOREIGN KEY (vin) REFERENCES Vehicle(vin);
  
ALTER TABLE Vehicle
  ADD CONSTRAINT fk_Vehicle_vehicleType_VehicleType_vehicleType FOREIGN KEY (vehicle_type) REFERENCES VehicleType(vehicle_type),
  ADD CONSTRAINT fk_Vehicle_manufacturerName_VehicleManufacturer_manufacturerName FOREIGN KEY (manufacturer_name) REFERENCES VehicleManufacturer(manufacturer_name);

ALTER TABLE Sell
  ADD CONSTRAINT ck_Sell_vehicleCondition CHECK (vehicle_condition in ('Excellent', 'Very Good', 'Good', 'Fair'));

ALTER TABLE Vehicle
  ADD CONSTRAINT ck_Vehicle_modelYear_fourDigits CHECK (model_year <= date_part('year', current_date)::numeric::int + 1);
  
CREATE TABLE if not exists Owner (
  username varchar(250) NOT NULL,
  password varchar(250) NOT NULL,
  first_name varchar(250) NOT NULL,
  last_name varchar(250) NOT NULL,
  PRIMARY KEY (username)
);

create or replace table Color (
  color varchar(50) primary key
);

-- overall user table
create or replace view public.user as 
select 
  username,
  password,
  first_name,
  last_name,
  'Admin' as user_role
from public.adminuser
union
select 
  username,
  password,
  first_name,
  last_name,
  'InventoryClerk' as user_role
from public.inventoryclerk
union
select
  username,
  password,
  first_name,
  last_name,
  'Manager' as user_role
from public.manager
union
select
  username,
  password,
  first_name,
  last_name,
  'InventoryClerk' as user_role
from public.inventoryclerk
union
select
  username,
  password,
  first_name,
  last_name,
  'Owner' as user_role
from public.owner;

-- seller history
create or replace view public.seller_history as
select
  ci.first_name || ' ' || ci.last_name as seller_name,
  count(s.vin) as number_of_vehicles_sold,
  avg(s.purchase_price) as average_purchase_price,
  sum(p.quantity) / count(s.vin) as average_number_of_parts_per_vehicle,
  sum(p.cost * p.quantity) / count(s.vin) as average_cost_of_parts_per_vehicle
from sell s
inner join customerindividual ci on ci.customer_id = s.customer_id
left join partorder po on po.vin = s.vin
left join part p on p.purchase_order_number = po.purchase_order_number
group by seller_name
union
select
  cb.tax_id_number as seller_name,
  count(s.vin) as number_of_vehicles_sold,
  avg(s.purchase_price) as average_purchase_price,
  sum(p.quantity) / count(s.vin) as average_number_of_parts_per_vehicle,
  sum(p.cost * p.quantity) / count(s.vin) as average_cost_of_parts_per_vehicle
from sell s
inner join customerbusiness cb on cb.customer_id = s.customer_id
left join partorder po on po.vin = s.vin
left join part p on p.purchase_order_number = po.purchase_order_number
group by seller_name;

-- average time in Inventory
create or replace view public.average_time_in_inventory as
select
  vt.vehicle_type,
  avg(date_part('Day', s.purchase_date::timestamp - b.sale_date::timestamp) + 1) as average_days_in_inventory
from vehicletype vt
left join vehicle v on v.vehicle_type = vt.vehicle_type
left join buy b on b.vin = v.vin
left join sell s on s.vin = v.vin
group by vt.vehicle_type;


-- price per condition
create or replace view public.price_per_condition as
with all_vehicle_conditions as (
  select cond as vehicle_condition
  from (values ('Excellent'), ('Very Good'), ('Good'), ('Fair')) t(cond)
),
cond_and_type as (
  select
    vt.vehicle_type,
    avc.vehicle_condition
  from all_vehicle_conditions avc
  cross join vehicletype vt
),
augmented_sell as (
  select
    s.vin,
    s.purchase_price,
    s.vehicle_condition,
    v.vehicle_type
  from sell s
  natural join vehicle v
)
select
  cond_and_type.vehicle_type,
  cond_and_type.vehicle_condition,
  avg(augmented_sell.purchase_price) as avg_purchase_price
from cond_and_type
left join augmented_sell
on cond_and_type.vehicle_type = augmented_sell.vehicle_type and
   cond_and_type.vehicle_condition = augmented_sell.vehicle_condition
group by 
  cond_and_type.vehicle_type,
  cond_and_type.vehicle_condition;
  

-- parts statistics
create or replace view public.parts_statistics as
select
  pv.name,
  sum(quantity) as total_number_of_parts,
  sum(total_cost) as total_dollar_amount
from partorder po
join partvendor pv on pv.name = po.part_vendor_name
natural join part p
group by pv.name;


-- monthly sales summary
-- calc per vehicle sale price, calc per vehicle cost, then join
create or replace view public.monthly_sales_summary as
with total_parts_cost_per_vehicle as (
  select
    buy.vin,
    sum(partorder.total_cost) * 1.10 as total_po_cost
  from buy
  natural join partorder
  group by buy.vin
),
purchase_price_per_vehicle as (
  select 
    date_part('year', buy.sale_date::date)::varchar as sale_year,
    date_part('month', buy.sale_date::date)::varchar as sale_month,
    buy.vin,
    sell.purchase_price
  from buy
  natural join sell
)
select
  pp.sale_year,
  pp.sale_month,
  count(pp.vin) as total_number_of_vehicles_sold,
  sum(pp.purchase_price) * 1.25 + sum(tc.total_po_cost) * 1.10 as total_sales_income,
  sum(pp.purchase_price) * 0.25 + sum(tc.total_po_cost) * 0.10 as total_net_income
from purchase_price_per_vehicle pp
natural join total_parts_cost_per_vehicle tc
group by pp.sale_year, pp.sale_month
order by pp.sale_year desc, pp.sale_month desc;


-- monthly sales drilldown - at this time, we know the year/month
create or replace view public.monthly_sales_drilldown as
with total_parts_cost_per_vehicle as (
  select
    buy.vin,
    sum(partorder.total_cost) * 1.10 as total_po_cost
  from buy
  natural join partorder
  group by buy.vin
)
select
  b.username,
  sp.first_name || ' ' || sp.last_name as sales_people,
  count(b.vin) as number_of_vehicles_sold,
  sum(s.purchase_price * 1.25) + sum(tc.total_po_cost) * 1.10 as sales_income
from buy b
natural join salespeople sp
natural join sell s
natural join total_parts_cost_per_vehicle tc
group by b.username, sales_people
order by number_of_vehicles_sold desc, sales_income desc;