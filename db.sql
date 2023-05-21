CREATE DATABASE IF NOT EXISTS thekitchenproject;
USE thekitchenproject;

DROP TABLE IF EXISTS mesas, pedidos, menu;

create table menu(
idComida int primary key auto_increment,
nombreComida varchar(50) not null,
precioComida numeric(6,2) not null
);
insert into menu(nombreComida, precioComida)
values ("taco de pastor", 13.00),
		("taco de cecina", 15.00),
        ("gringa", 35.00),
        ("torta de pastor", 45.00),
        ("torta de cecina", 45.00),
        ("torta mixta", 50.00),
        ("papa asada de pastor", 65.00),
        ("papa asada de cecina", 65.00),
        ("papa asada mixta", 70.00),
        ("coca cola 600ml", 28.00),
        ("pepsi 600ml", 26.00),
        ("sprite 600ml", 26.00),
        ("manzanita sol 600ml", 26.00);
        

create table mesas(
mesa int primary key
);
insert into mesas (mesa) values (1), (2), (3), (4), (5), (6), (7), (8), (9), (10);

create table pedidos(
noOrden int primary key auto_increment,
orden varchar(255) not null,
mesa int not null,
fecha varchar(10) not null,
hora varchar(8) not null,
estado varchar(25) not null,
foreign key (mesa) references mesas(mesa) on delete cascade on update cascade
);

insert into pedidos(noOrden, orden, mesa, fecha, hora, estado) values 
(1, "5 tacos de trompo s/cebolla", 3, "04/03/2023", "03:22:05", "Preparando"),
(2, "3 Tortas de trompo c/todo", 3, "04/03/2023", "03:28:54", "Preparando"),
(3, "4 tacos de trompo c/todo", 1, "04/03/2023", "03:51:32", "Preparando"),
(4, "1 papa asada de pastor ", 7, "04/03/2023", "04:01:43", "Preparando"),
(5, "1 gringa c/todo \n 3 tacos de trompo c/todo \n 3 tacos de trompo c/todo \n 3 tacos de trompo c/todo \n 3 tacos de trompo c/todo \n 3 tacos de trompo c/todo \n 3 tacos de trompo c/todo", 1, "04/03/2023", "04:04:47", "Preparando"),
(6, "5 tacos de trompo s/cebolla", 3, "04/03/2023", "04:17:18", "Preparando")

;


