
IF OBJECT_ID('menu', 'U') IS NOT NULL
    DROP TABLE menu;
IF OBJECT_ID('FK_pedidos_mesas', 'F') IS NOT NULL
    ALTER TABLE pedidos DROP CONSTRAINT FK_pedidos_mesas;

IF OBJECT_ID('mesas', 'U') IS NOT NULL
    DROP TABLE mesas;
IF OBJECT_ID('pedidos', 'U') IS NOT NULL
    DROP TABLE pedidos;

CREATE TABLE menu (
    idComida INT PRIMARY KEY IDENTITY(1,1),
    nombreComida VARCHAR(50) NOT NULL,
    precioComida DECIMAL(6, 2) NOT NULL
);

INSERT INTO menu (nombreComida, precioComida)
VALUES
    ('taco de pastor', 13.00),
    ('taco de cecina', 15.00),
    ('gringa', 35.00),
    ('torta de pastor', 45.00),
    ('torta de cecina', 45.00),
    ('torta mixta', 50.00),
    ('papa asada de pastor', 65.00),
    ('papa asada de cecina', 65.00),
    ('papa asada mixta', 70.00),
    ('coca cola 600ml', 28.00),
    ('pepsi 600ml', 26.00),
    ('sprite 600ml', 26.00),
    ('manzanita sol 600ml', 26.00);

CREATE TABLE mesas (
    mesa INT PRIMARY KEY
);

INSERT INTO mesas (mesa)
VALUES
    (1), (2), (3), (4), (5), (6), (7), (8), (9), (10);


CREATE TABLE pedidos (
    noOrden INT IDENTITY(1,1) PRIMARY KEY,
    orden VARCHAR(255) NOT NULL,
    mesa INT NOT NULL,
    fecha VARCHAR(10) NOT NULL,
    hora VARCHAR(8) NOT NULL,
    estado VARCHAR(25) NOT NULL,
    total DECIMAL(8, 2) NOT NULL,
    FOREIGN KEY (mesa) REFERENCES mesas (mesa)
);

INSERT INTO pedidos (orden, mesa, fecha, hora, estado, total)
VALUES
    ('5 tacos de trompo s/cebolla', 3, '04/03/2023', '03:22:05', 'Preparando', 00.00),
    ('3 Tortas de trompo c/todo', 3, '04/03/2023', '03:28:54', 'Preparando', 00.00),
    ('4 tacos de trompo c/todo', 1, '04/03/2023', '03:51:32', 'Preparando', 00.00),
    ('1 papa asada de pastor ', 7, '04/03/2023', '04:01:43', 'Preparando', 00.00),
    ('1 gringa c/todo \n 3 tacos de trompo c/todo \n 3 tacos de trompo c/todo \n 3 tacos de trompo c/todo \n 3 tacos de trompo c/todo \n 3 tacos de trompo c/todo \n 3 tacos de trompo c/todo', 1, '04/03/2023', '04:04:47', 'Preparando', 00.00),
    ('5 tacos de trompo s/cebolla', 3, '04/03/2023', '04:17:18', 'Preparando', 00.00);