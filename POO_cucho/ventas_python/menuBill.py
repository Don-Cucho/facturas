from components import Menu,Valida
from utilities import borrarPantalla,gotoxy
from utilities import reset_color,red_color,green_color,yellow_color,blue_color,purple_color,cyan_color
from clsJson import JsonFile
from company  import Company
from customer import RegularClient
from sales import Sale
from product  import Product
from iCrud import ICrud
import datetime
import time,os
from functools import reduce
from customer import RegularClient, VipClient

path, _ = os.path.split(os.path.abspath(__file__))
# Procesos de las Opciones del Menu Facturacion
class CrudClients(ICrud):
    def create(self):
        validar = Valida()
        print('\033c', end='')
        gotoxy(2,1);print("█"+green_color+"█"*90)
        gotoxy(2,2);print("██"+" "*34+"Consulta de Cliente"+" "*35+"██")
        gotoxy(2,4);print("Ingrese el DNI: ",end="")
        gotoxy(2,4);dni=validar.cedula("Error: Cedula Invalida",18,4)
        json_file = JsonFile(path+'/archivos/clients.json')
        exists = json_file.find("dni",dni)
        if exists:
            gotoxy(25,7);print("Usuario ya existente")
            time.sleep(2)
            return
        gotoxy(2,5);print("Ingrese su Nombre: ",end="")
        gotoxy(2,5);nombre = validar.solo_letras("Error: Solo Letras",22,5).lower().capitalize()
        gotoxy(2,6);print("Ingrese su Apellido: ",end="")
        gotoxy(2,6);apellido= validar.solo_letras("Error: Solo Letras",23,6).lower().capitalize()
        gotoxy(2,7);print("Es VIP? (s/n): ",end="")
        gotoxy(2,7);es_vip = validar.solo_letras("Error: Solo 's' o 'n' ",22,7).lower()
        if es_vip == "s" or es_vip == "si":
            valor = 10000
            cliente = VipClient(first_name=nombre, last_name=apellido, dni=dni)
            cliente.limit = valor
        else:
            gotoxy(2,7);print("¿Tiene tarjeta de descuento? (s/n): ",end="")
            gotoxy(2,7);tiene_tarjeta = validar.solo_letras("Error: Solo 's' o 'n' ",41,7).lower()
            if tiene_tarjeta == "s" or tiene_tarjeta == "si":
                card = True
            else:
                card = False
            cliente = RegularClient(first_name=nombre, last_name=apellido, dni=dni, card=card)
            valor = cliente.discount
        client = {"dni": dni,"nombre": nombre, "apellido": apellido,"valor": valor}
        if client['dni'] != "" and client['nombre'] != "" and client['apellido'] != "":
            gotoxy(2,9);print("Guardar al Cliente presione (s/n)")
            gotoxy(2,9);valida= validar.solo_letras("Error: Solo 's' o 'n' ",36,9).lower()
            if valida == "s" or valida == "si":
                cli = json_file.read()
                clin = cli
                clin.append(client)
                json_file.save(clin)
                gotoxy(48,12);print("Cliente Agregado Con Exito")
                time.sleep(2)
            else:
                gotoxy(24,10);print("Accion Eliminada")
                time.sleep(1)
        else:
            print("No se llenaron los datos")        
            time.sleep(1)

    def update(self):
        validar = Valida()
        print('\033c', end='')
        gotoxy(2,1);print(green_color+"█"*90)
        gotoxy(2,2);print("██"+" "*34+"Actualizar Cliente"+" "*35+"██")
        print("Ingrese dni del cliente a actualizar: ")
        gotoxy(2,4);client_dni = validar.solo_numeros("Error: Solo Numeros",39,3)
        json_file = JsonFile(path+'/archivos/clients.json')
        dato = json_file.read()
        clients = json_file.find("dni", client_dni)
        
        if not clients:
            print(f"No se encontró al cliente con el DNI: {client_dni}")
            time.sleep(1)
            return
        
        client_index = None
        
        for idx, client in enumerate(dato):
            if client["dni"] == client_dni:
                client_index = idx
                break
        
        if client_index is not None:
            client = dato[client_index]
            valor_actual_nombre=client["nombre"]
            valor_actual_apellido=client["apellido"]
            gotoxy(15,5);print("Cliente")
            gotoxy(35,5);print("Apellido")
            gotoxy(55,5);print("Valor")
            gotoxy(15,6);print(f"{client['nombre']:}")
            gotoxy(35,6);print(f"{client['apellido']}")
            gotoxy(55,6);print(f"{client['valor']}")
            print("Ingrese el nuevo nombre (Deje vacío para mantener el mismo): ")
            new_nombre = validar.solo_letras_and_espacios("Error: Solo Letras",62,7,valor_actual_nombre).lower().capitalize()
            print("Ingrese el nuevo apellido (Deje vacío para mantener el mismo): ")
            new_apellido = validar.solo_letras_and_espacios("Error: Solo Letras",64,8,valor_actual_apellido).lower().capitalize()
            print("Quiere ser cliente VIP? (s/n): ",end="")
            tiene_tarjeta = validar.solo_letras("Error: Solo 's' o 'n' ",32,9).lower()
            
            if tiene_tarjeta == "s" or tiene_tarjeta == "si":
                cliente = VipClient(first_name=new_nombre, last_name=new_apellido, dni=client_dni)
                cliente.limit = 10000
            else:
                print("¿Tiene tarjeta de descuento? (s/n): ",end="")
                tarjeta_descuento = validar.solo_letras("Error: Solo 's' o 'n' ",37,10).lower()
                if tarjeta_descuento == "si" or tarjeta_descuento == "s":
                    card=True
                else:
                    card=False
                cliente = RegularClient(first_name=new_nombre, last_name=new_apellido, dni=client_dni, card=card)
            dato[client_index] = cliente.getJson()
            json_file.save(dato)
            gotoxy(55,13);print("Cliente actualizado exitosamente.")
            time.sleep(2)
        else:
            print(f"No se encontró al cliente con el DNI: {client_dni}")
            time.sleep(1)

    def delete(self):
        borrarPantalla()
        validar = Valida()
        print('\033c', end='')
        gotoxy(2, 1); print("█" + green_color + "█" * 90)
        gotoxy(2, 2); print("██" + " " * 34 + "Eliminación de Cliente" + " " * 34 + "██")
        gotoxy(2, 4); print("Ingrese DNI del cliente a eliminar:  ")
        gotoxy(2, 4); dni = validar.solo_numeros("Error: Solo Numeros",37,4)
        json_file = JsonFile(path+'/archivos/clients.json')
        dato=json_file.read()
        clients = json_file.find("dni", dni)
        if clients:
            dato.remove(clients[0])
            client=clients[0]
            gotoxy(15,5);print("------------------ Eliminar Cliente ------------------")
            gotoxy(15,6);print("Cliente")
            gotoxy(35,6);print("Apellido")
            gotoxy(55,6);print("Valor")
            gotoxy(15,7);print(f"¦¦{client['nombre']:}¦¦")
            gotoxy(35,7);print(f"¦¦{client['apellido']}¦¦")
            gotoxy(55,7);print(f"¦¦{client['valor']}¦¦")
            gotoxy(15,8);print("-------------------------------------------------------")
            gotoxy(2,9);print("⚠️ Elminar Producto: Presione (s)⚠️ : ")
            gotoxy(2,9);valido = validar.solo_letras("Error Solo letras",38,9)
            if valido == "s":
                json_file.save(dato)
                gotoxy(15,11);print("✔✔ Cliente eliminado exitosamente ✔✔")
                time.sleep(2)
            else:
                gotoxy(15,10);print("Accion Eliminada")
                time.sleep(1)
                return
        else:
            gotoxy(10,6);print("Usuario inexistente.")
            time.sleep(1)

    def consult(self):
        validar = Valida()
        print('\033c', end='')
        gotoxy(2,1);print(green_color+"█"*90)
        gotoxy(2,2);print("██"+" "*34+"Consulta de Cliente"+" "*35+"██")
        print("¿Qué tipo de cliente desea consultar?")
        print("1. VIP")
        print("2. Regular")
        print("3. Consutar a uno en especifico:")
        gotoxy(2,7);print("Elija una opcion:")
        tipo_cliente = validar.solo_numeros("Error: Ingrese 1 o 2 o 3", 19, 7)
        json_file = JsonFile(path+'/archivos/clients.json')
        clients = []
        if tipo_cliente == "1":
            clients_vip = json_file.find("valor", 10000)
            clients.extend(clients_vip)
            gotoxy(15,10);print("DNI")
            gotoxy(35,10);print("Cliente")
            gotoxy(55,10);print("Apellido")
            gotoxy(75,10);print("Valor")
            linea = 0
            for client in clients:
                gotoxy(15,11+linea);print(f"{client['dni']:}")
                gotoxy(36,11+linea);print(f"{client['nombre']:}")
                gotoxy(56,11+linea);print(f"{client['apellido']}")
                gotoxy(75,11+linea);print(f"{client['valor']}")
                linea+=1
            time.sleep(2)
        elif tipo_cliente == "2":
            clients_1 = json_file.find("valor", 0.1)
            clients_0 = json_file.find("valor", 0)
            clients.extend(clients_0)
            clients.extend(clients_1)
            gotoxy(15,10);print("DNI")
            gotoxy(35,10);print("Cliente")
            gotoxy(55,10);print("Apellido")
            gotoxy(75,10);print("Valor")
            linea = 0
            for client in clients:
                gotoxy(15,11+linea);print(f"{client['dni']:}")
                gotoxy(36,11+linea);print(f"{client['nombre']:}")
                gotoxy(56,11+linea);print(f"{client['apellido']}")
                gotoxy(76,11+linea);print(f"{client['valor']}")
                linea+=1
            time.sleep(2)
        elif tipo_cliente == "3":
            json_file = JsonFile(path+'/archivos/clients.json')
            clients1 = json_file.read()
            print("Ingrese el DNI que desea consultar: ")
            gotoxy(2,4);client= validar.solo_numeros("Error: Solo Numeros",37,8)
            for dni in clients1:
                if dni["dni"] == client:
                    gotoxy(15,10);print("DNI")
                    gotoxy(35,10);print("Cliente")
                    gotoxy(55,10);print("Apellido")
                    gotoxy(75,10);print("Valor")
                    gotoxy(15,11);print(f"{dni['dni']:}")
                    gotoxy(36,11);print(f"{dni['nombre']:}")
                    gotoxy(56,11);print(f"{dni['apellido']}")
                    gotoxy(76,11);print(f"{dni['valor']}")
                    time.sleep(2)
                    break
            else:
                print(f"No se encontró al cliente con el DNI: {client}")
            time.sleep(1)
        elif tipo_cliente != "1" and "2" and "3":
            print("Opcion no valida")

class CrudProducts(ICrud):
    def create(self):
        borrarPantalla()
        validar=Valida()
        print('\033c', end='')
        gotoxy(2,1);print("█"+green_color+"█"*90)
        gotoxy(2,2);print("██"+" "*34+"Crear Producto"+" "*35+"██")
        gotoxy(2,4);print("Ingrese nombre del producto: ")
        gotoxy(2,4);descripcion=validar.solo_letras("Error: Solo Letras",32,4).lower().capitalize()
        
        json_file = JsonFile(path+'/archivos/products.json')
        dato = json_file.read()
        buscar =json_file.find("descripcion",descripcion)
        if buscar:
            gotoxy(2,5);print(f"Producto ya Existente {descripcion} ")
            input("Presione una tecla para salir...") 
            return

        gotoxy(2,5);print("Ingrese Precio: ")
        gotoxy(2,5);precio= validar.solo_decimales("Error: Solo Numeros",19,5)
        
        gotoxy(2,6);print("Ingrese Cantidad del Stock: ")
        gotoxy(2,6);stock = validar.solo_decimales("Error: Solo Numeros",30,6)

        ids = [producto["id"] for producto in dato if "id" in producto]
        ultimo_id = max(ids)+ 1
        producto = Product(ultimo_id,descripcion,precio,stock)
        product = producto.getJson()

        if product['descripcion'] != "" and product['precio'] != "" and product["stock"] != "":
            gotoxy(2,7);valida = input("Guardar el Producto presione (s/n)")
            if valida == "s":
                produ = dato
                produ.append(product)
                json_file.save(produ)
                gotoxy(15,10);print("------------------ Producto -----------------")
                gotoxy(15,11);print("Producto   ")
                gotoxy(35,11);print("   Precio   ")
                gotoxy(55,11);print("   Stock  ")
                gotoxy(15,12);print(f"¦¦{descripcion}¦¦")
                gotoxy(35,12);print(f"¦¦{precio}     ¦¦")
                gotoxy(55,12);print(f"¦¦{stock}      ¦¦")
                gotoxy(15,13);print("---------------------------------------------")
                gotoxy(24,15);print("✔✔ Producto agragado con Exito ✔✔")
                input("Presione una tecla para salir...")
            else:
                gotoxy(24,9);print("Accion Elimina")
                time.sleep(1)
        else:
            print("No se llenaron los datos")
            time.sleep(1)

    def update(self):
        borrarPantalla()
        validar = Valida()
        print('\033c', end='')
        gotoxy(2,1);print("█"+ green_color+"█"*90)
        gotoxy(2,2);print("██"+" "*34+"Actualizar Cliente"+" "*35+"██")
        gotoxy(2,4);print("Ingrese id del Producto a actualizar: ")
        gotoxy(2,4);producto_id = validar.solo_numeros("Error: Solo Numeros",40,4)
        product_id = int(producto_id)
        json_file = JsonFile(path+'/archivos/products.json')
        dato = json_file.read()
        product = json_file.find("id", product_id)

        if not product:
            print(f"No se encontró el producto con el ID: {product_id}")
            time.sleep(1)
            return

        producto_index = None

        for index, products in enumerate(dato):#para conocer la posición en la que se encientra el producto
            if products["id"] == product_id:
                producto_index = index
                break

        if producto_index is not None:
            products = dato[producto_index]
            gotoxy(15,6);print("------------------ Producto Encontrado -----------------")
            gotoxy(15,7);print("Producto   ")
            gotoxy(35,7);print("   Precio   ")
            gotoxy(55,7);print("   Stock  ")
            gotoxy(15,8);print(f"¦¦{products['descripcion']}¦¦")
            gotoxy(35,8);print(f"¦¦{products['precio']}     ¦¦")
            gotoxy(55,8);print(f"¦¦{products['stock']}      ¦¦")
            gotoxy(15,9);print("-"*55)
            valor_actual_nombre=products["descripcion"]
            valor_actual_precio=products["precio"]
            valor_actual_stock=products["stock"]
            
            gotoxy(3,10);print("Ingrese el nuevo nombre (Deje vacío para mantener el mismo): ")
            new_nombre = validar.solo_letras_and_espacios("Error: Solo Letras",62,10,valor_actual_nombre).lower().capitalize()
            gotoxy(3,11);print("Ingrese el nuevo precio (Deje vacío para mantener el mismo): ")
            new_precio = validar.solo_decimales_and_espacios("Error: Solo Numeros",62,11,valor_actual_precio)
            gotoxy(3,12);print("Ingrese el nuevo stock (Deje vacío para mantener el mismo): ")
            new_stock = validar.solo_decimales_and_espacios("Error: Solo Numeros",61,12,valor_actual_stock)
            
            products["descripcion"] = new_nombre
            
            products["precio"] = new_precio
            
            products["stock"] = new_stock
            
            dato[producto_index] = products
            json_file.save(dato)
            gotoxy(15,15);print("✔✔ Producto actualizado exitosamente ✔✔")
            time.sleep(2)
        else:
            print(f"No se encontró el producto con el ID: {producto_id}")
            time.sleep(1)

    def delete(self):
        borrarPantalla()
        validar = Valida()
        print('\033c', end='')
        gotoxy(2,1);print(green_color+"█"*90)
        gotoxy(2,2);print("██"+" "*34+"Eliminar un Producto"+" "*35+"██")
        gotoxy(2,4);print("Ingrese nombre del producto: ")
        gotoxy(2,4);producto= validar.solo_letras("Error: Solo Letras",30,4).lower().capitalize()
        json_file = JsonFile(path+'/archivos/products.json')
        dato=json_file.read()
        products = json_file.find("descripcion",producto)

        if products:
            product=products[0]
            gotoxy(15,6);print("------------------ Producto Encontrado -----------------")
            gotoxy(15,7);print("Producto   ")
            gotoxy(35,7);print("   Precio   ")
            gotoxy(55,7);print("   Stock  ")
            gotoxy(15,8);print(f"¦¦{product['descripcion']}¦¦")
            gotoxy(35,8);print(f"¦¦{product['precio']}     ¦¦")
            gotoxy(55,8);print(f"¦¦{product['stock']}      ¦¦")
            gotoxy(15,9);print("---------------------------------------------")
            gotoxy(2,10);print("⚠️ Elminar Producto: Presione (s)⚠️ : ")
            gotoxy(2,10);valido = validar.solo_letras("Error Solo letras",38,10)
            if valido == "s":
                dato.remove(products[0])
                gotoxy(15,12);print(f"✔✔ Producto eliminado Exitosamente ✔✔")
                json_file.save(dato)
                time.sleep(2)
            else:
                gotoxy(15,12);print("Accion Cacelada")
                time.sleep(1)
                return
        else:
            print(f"No se encontró el producto con el nombre: {producto}")
            time.sleep(1)

    def consult(self):
        borrarPantalla()
        validar = Valida()
        print('\033c', end='')
        gotoxy(2,1);print(green_color+"█"*90)
        gotoxy(2,2);print("██"+" "*34+"Consulta del Producto"+" "*35+"██")
        gotoxy(2,4);print("Ingrese nombre del producto: ")
        gotoxy(2,4);producto= validar.solo_letras("Error ingrese solo letras",30,4).lower().capitalize()
        json_file = JsonFile(path+'/archivos/products.json')
        products = json_file.find("descripcion",producto)
        if products:
            product=products[0]
            gotoxy(15,6);print("----------------------- Producto Encontrado ---------------------")
            gotoxy(15,7);print("  id ")
            gotoxy(35,7);print("Producto   ")
            gotoxy(55,7);print("   Precio   ")
            gotoxy(75,7);print("   Stock  ")
            gotoxy(15,8);print(f"¦¦{product['id']}         ¦¦")
            gotoxy(35,8);print(f"¦¦{product['descripcion']}¦¦")
            gotoxy(55,8);print(f"¦¦{product['precio']}     ¦¦")
            gotoxy(75,8);print(f"¦¦{product['stock']}      ¦¦")
            gotoxy(15,9);print("-----------------------------------------------------------------")
            time.sleep(4)
        else:
            print(f"No se encontró al Producto con el nombre: {producto}")
            time.sleep(1)


class CrudSales(ICrud):
    def create(self):
        # cabecera de la venta
        validar = Valida()
        borrarPantalla()
        print('\033c', end='')
        gotoxy(2,1);print(green_color+"*"*90+reset_color)
        gotoxy(30,2);print(blue_color+"Registro de Venta")
        gotoxy(17,3);print(blue_color+Company.get_business_name())
        gotoxy(5,4);print(f"Factura#:F0999999 {' '*3} Fecha:{datetime.datetime.now()}")
        gotoxy(66,4);print("Subtotal:")
        gotoxy(66,5);print("Decuento:")
        gotoxy(66,6);print("Iva     :")
        gotoxy(66,7);print("Total   :")
        gotoxy(15,6);print("Cedula:")
        dni=validar.solo_numeros("Error: Solo numeros",23,6)
        json_file = JsonFile(path+'/archivos/clients.json')
        client = json_file.find("dni",dni)
        if not client:
            gotoxy(35,6);print("Cliente no existe")
            return
        client = client[0]
        cli = RegularClient(client["nombre"],client["apellido"], client["dni"], card=True) 
        sale = Sale(cli)
        gotoxy(35,6);print(cli.fullName())
        gotoxy(2,8);print(green_color+"*"*90+reset_color) 
        gotoxy(5,9);print(purple_color+"Linea") 
        gotoxy(12,9);print("Id_Articulo") 
        gotoxy(24,9);print("Descripcion") 
        gotoxy(38,9);print("Precio") 
        gotoxy(48,9);print("Cantidad") 
        gotoxy(58,9);print("Subtotal") 
        gotoxy(70,9);print("n->Terminar Venta)"+reset_color)
        # detalle de la venta
        follow ="s"
        line=1
        while follow.lower()=="s":
            gotoxy(7,9+line);print(line)
            gotoxy(15,9+line)
            id=int(validar.solo_numeros("Error: Solo numeros",15,9+line))
            json_file = JsonFile(path+'/archivos/products.json')
            prods = json_file.find("id",id)
            if not prods:
                gotoxy(24,9+line);print("Producto no existe")
                time.sleep(1)
                gotoxy(24,9+line);print(" "*20)
            else:    
                prods = prods[0]
                product = Product(prods["id"],prods["descripcion"],prods["precio"],prods["stock"])
                gotoxy(24,9+line);print(product.descrip)
                gotoxy(38,9+line);print(product.preci)
                gotoxy(49,9+line);qyt=int(validar.solo_numeros("Error:Solo numeros",49,9+line))
                gotoxy(59,9+line);print(product.preci*qyt)
                sale.add_detail(product,qyt)
                gotoxy(76,4);print(round(sale.subtotal,2))
                gotoxy(76,5);print(round(sale.discount,2))
                gotoxy(76,6);print(round(sale.iva,2))
                gotoxy(76,7);print(round(sale.total,2))
                gotoxy(74,9+line);follow=input() or "s"  
                gotoxy(76,9+line);print(green_color+"✔"+reset_color)  
                line += 1
        gotoxy(15,9+line);print(red_color+"Esta seguro de grabar la venta(s/n):")
        gotoxy(54,9+line);procesar = validar.solo_letras("Error: Solo Letras",53,9+line).lower()
        if procesar == "s" or procesar == "si":
            gotoxy(15,10+line);print("😊 Venta Grabada satisfactoriamente 😊"+reset_color)
            # print(sale.getJson())  
            json_file = JsonFile(path+'/archivos/invoices.json')
            invoices = json_file.read()
            ult_invoices = invoices[-1]["factura"]+1
            data = sale.getJson()
            data["factura"]=ult_invoices
            invoices.append(data)
            json_file = JsonFile(path+'/archivos/invoices.json')
            json_file.save(invoices)
        else:
            gotoxy(20,10+line);print("🤣 Venta Cancelada 🤣"+reset_color)    
        time.sleep(2)  

    def update(self): 
        validar = Valida()
        sale = Sale
        print('\033c', end='')
        gotoxy(2,1);print(green_color+"█"*90)
        gotoxy(2,2);print("██"+" "*34+"Actualización de Factura"+" "*35+"██")
        gotoxy(2,4);print("Ingrese el número de factura a actualizar: ")
        gotoxy(2,4);invoice_num = validar.solo_numeros("Error: Solo Numeros",47,4)
        invoice_number = int(invoice_num)
        json_file = JsonFile(path+'/archivos/invoices.json')
        invoices = json_file.read()
        busqueda = json_file.find("factura",invoice_number)

        invoices_index = None
        for index, products in enumerate(invoices):#para conocer la posición en la que se encientra el producto
            if products["factura"] == invoice_number:
                invoices_index = index
                break
        
        if invoices_index is not None:
            invoce = invoices[invoices_index]
            gotoxy(20,5);print(f"Impresion de la Factura# {invoice_num}")
            gotoxy(13,6);print("----------------------------- Factura Encontrada ---------------------------")
            gotoxy(13,7);print("Factura    ")
            gotoxy(26,7);print("Fecha      ")
            gotoxy(39,7);print("Cliente    ")
            gotoxy(52,7);print("Subtotal   ")
            gotoxy(65,7);print("Descuento  ")
            gotoxy(78,7);print("IVA        ")
            gotoxy(91,7);print("Total  ")
            gotoxy(13,8);print(f"¦¦{invoce['factura']}  ¦¦")
            gotoxy(26,8);print(f"¦¦{invoce['Fecha']}    ¦¦")
            gotoxy(39,8);print(f"¦¦{invoce['cliente']}  ¦¦")
            gotoxy(52,8);print(f"¦¦{invoce['subtotal']} ¦¦")
            gotoxy(65,8);print(f"¦¦{invoce['descuento']}¦¦")
            gotoxy(78,8);print(f"¦¦{invoce['iva']}      ¦¦")
            gotoxy(91,8);print(f"¦¦{invoce['total']}    ¦¦")
            gotoxy(13,9);print("-"*75)   
            gotoxy(2,11);print(green_color+"█"*90)
            gotoxy(2,12);print("¿Qué desea actualizar?")
            gotoxy(2,13);print("1. Fecha")
            gotoxy(2,14);print("2. Cliente")
            gotoxy(2,15);print("3. Subtotal")
            gotoxy(2,16);print("4. Descuento")
            gotoxy(2,17);print("5. Iva")
            gotoxy(2,18);print("6. Total")
            gotoxy(2,19);print("7. Detalle (Agregar/Actualizar/Eliminar)")
            gotoxy(2,20);print("8. Cancelar")
            gotoxy(10,22);print('Seleccione una opcion:',end="")
            gotoxy(10,22);opcion = validar.solo_numeros("Error: Solo numeros",34, 22)
            if opcion == '1':
                gotoxy(10,22);print("Ingrese la nueva fecha (YYYY-MM-DD): ")
                gotoxy(10,22);nueva_fecha = validar.solo_fecha("Error: Solo Formato de Fecha",47, 22)
                invoce["Fecha"] = nueva_fecha
                json_file.save(invoices)
            elif opcion == '2':
                gotoxy(2,24);print("Ingrese el DNI del cliente: ")
                gotoxy(2,24);dni = validar.solo_numeros("Error: Solo numeros",28,24)
                json_file3 = JsonFile(path+'/archivos/clients.json')
                busqueda = json_file3.find("dni",dni)
                if not busqueda:
                        gotoxy(10,25);print("Cliente no existe")
                        time.sleep(2)
                        return
                invoce["cliente"] = busqueda[0]["nombre"]
                json_file.save(invoices)
                print("Cliente Actualizado ")
            elif opcion == '3':# como actualizo el subtotal si eso es con los productos automatico
                gotoxy(2,24);print("Ingrese el nuevo subtotal: ")
                gotoxy(2,24);nuevo_subtotal = validar.solo_decimales("Error: Solo numeros",28,24) 
                invoce["subtotal"] = float(nuevo_subtotal)
                json_file.save(invoices)
            elif opcion == '4':
                gotoxy(2,24);print("Ingrese el nuevo descuento en numero entero: ")
                gotoxy(2,24);nuevo_descuento = validar.solo_numeros("Error: Solo numeros",49,24) 
                invoce["descuento"] = int(nuevo_descuento)/100
                invoce["iva"] = round(0.12*invoce["subtotal"],2)
                invoce["total"]= round(invoce["iva"]+invoce["subtotal"]-invoce["descuento"],2)
                json_file.save(invoices)
            elif opcion == '5':
                gotoxy(2,24);print("Ingrese el nuevo IVA en porcetaje en numero entero: ")
                gotoxy(2,24);nuevo_iva = validar.solo_numeros("Error: Solo numeros",49,24) 
                invoce["iva"] = round((int(nuevo_iva)/100)*invoce["subtotal"],2)
                invoce["total"]= round(invoce["iva"]+invoce["subtotal"]-invoce["descuento"],2)
                json_file.save(invoices)
            elif opcion == '6':# como actualizo el total si eso es con los productos automatico
                gotoxy(2,24);print("Ingrese el nuevo total: ")
                gotoxy(2,24);nuevo_total = validar.solo_decimales("Error: Solo numeros",28,24)
                invoce["total"] = float(nuevo_total)
                json_file.save(invoices)
            elif opcion == '7':
                subopcion = input("¿Qué desea hacer en el detalle? ( 1)agregar / 2)actualizar / 3)eliminar): ")
                gotoxy(2,24);print(green_color+"█"*92)
                gotoxy(2,25);print("██"+" "*24+"Actualización de los Productos de Factura"+" "*23+"██") 
                gotoxy(13,26);print("---------------------------------- Detalles -------------------------------")
                detalles=invoices[invoices_index]["detalle"]
                gotoxy(8 ,28);print("Detalle   ")
                gotoxy(13,28);print("Producto   ")
                gotoxy(26,28);print("Precio     ")
                gotoxy(39,28);print("Cantidad   ")
                linea=1
                for x in detalles:
                    gotoxy(8,29+linea);print(linea)
                    gotoxy(13,29+linea);print(x["poducto"])
                    gotoxy(26,29+linea);print(x["precio"])
                    gotoxy(39,29+linea);print(x["cantidad"])
                    linea+=1
                gotoxy(13,30+linea);print("-"*75)   
                if subopcion == '1':
                    # Agregar nuevo producto al detalle
                    gotoxy(2,31+linea);print("Ingrese el nombre del producto: ")
                    producto_nuevo = validar.solo_letras("Error: Solo Letras",33,31+linea).lower().capitalize()
                    json_file1 = JsonFile(path+'/archivos/products.json')
                    product = json_file1.find("descripcion",producto_nuevo)
                    
                    if not product:
                        print("producto no existe")
                        return
                  
                    produc = product[0]
                    gotoxy(2,33+linea);print(f'Precio del producto: {produc['precio']}')
                    gotoxy(2,34+linea);print("Ingrese la cantidad del producto: ")
                    cantidad = validar.solo_numeros("Error: Solo Numeros",35,34)
                    detalle = {"poducto": producto_nuevo, "precio": produc['precio'], "cantidad": cantidad}
                    gotoxy(2,35+linea);print("Seguro que quiere agregarlo (s/n)")
                    valida = validar.solo_letras("Error solo letras",34,35+linea).lower()
                    if valida == "si" or "s":
                      detalles.append(detalle)
                      subtotal, discount, iva, total = sale.cal(detalles)
                      invoce["subtotal"] = round(subtotal, 2)
                      invoce["descuento"] = round(discount, 2)
                      invoce["iva"] = round(iva, 2)
                      invoce["total"] = round(total, 2)
                      gotoxy(10,37+linea);print("Producto agregado al detalle.")
                      json_file.save(invoices)
                    else:
                        print("Accion Elimina ")
                    
                elif subopcion == '2':
                    # Mostrar detalle actual y permitir actualizar precio o cantidad
                    producto_encontrado = False
                    gotoxy(2,31+linea);print('Qué producto quiere actualizar (Ingrese el nombre): ')
                    subopcion_update = validar.solo_letras("Error: Solo Letras",54,31+linea).lower().capitalize()
                    for product in detalles:
                      if product["poducto"] == subopcion_update:
                        producto_encontrado = True
                        print("Por cual producto lo quiere remplazar:")
                        produ=validar.solo_letras("Error solo letras",41,33+linea).lower().capitalize()
                        json_fil2 = JsonFile(path+'/archivos/products.json')
                        productBus = json_fil2.find("descripcion",produ)
                        if productBus == []:
                            print(f"producto no existe {produ}")
                            return
                        
                        produc = productBus[0]
                        gotoxy(13,32);print("Producto   ")
                        gotoxy(26,32);print("Precio     ")
                        gotoxy(13,33);print(produc["descripcion"])
                        gotoxy(26,33);print(produc["precio"])
                        
                        gotoxy(2,34+linea);print("Ingrese la cantidad del producto: ")
                        cantidad = validar.solo_numeros("Error: Solo Numeros",35,34)
                        
                        product["poducto"] = produc["descripcion"] 
                        
                        product["precio"] = float(produc["precio"] ) 
                        
                        product["cantidad"] = int(cantidad)
                        
                        gotoxy(2,35+linea);print("Seguro que quiere agregarlo (s/n)")
                        valida = validar.solo_letras("Error solo letras",34,35+linea).lower()
                        if valida == "si" or "s":
                            subtotal, discount, iva, total = sale.cal(detalles)
                            invoce["subtotal"] = round(subtotal, 2)
                            invoce["descuento"] = round(discount, 2)
                            invoce["iva"] = round(iva, 2)
                            invoce["total"] = round(total, 2)
                            gotoxy(10,37+linea);print("Producto Actualizado.")
                            json_file.save(invoices)
                            break
                        else:
                            print("Accion Elimina ")
                    if not producto_encontrado:
                        print(f"Producto no encontrado.{subopcion_update}")
                elif subopcion == '3':#poner GOTOXY y modificar lineas
                    # Mostrar detalle actual y permitir eliminar un producto
                    bandera=True
                    producto_encontrado = False
                    while bandera:
                        print('Qué producto quiere eliminar (Ingrese el nombre): ')
                        subopcion_update = validar.solo_letras("Error: Solo letras", 51, 30+linea).lower().capitalize()
                        for i, product in enumerate(detalles):
                            if len(detalles) == 1:
                                gotoxy(2,32+linea);print("¡Atención! Esta factura será Anulada Porque solo tiene un producto y esta eliminandolo")
                                gotoxy(2,32+linea);print("¿Está seguro? (s/n):")
                                confirmacion = validar.solo_letras("Error solo letras",22,32+linea)
                                if confirmacion.lower() == 's':
                                    invoices.remove(busqueda[0])
                                    json_file.save(invoices)
                                    bandera = False
                                    print("Factura eliminada.")
                                else:
                                    print("Cancelando eliminación de factura.")
                                
                            if product["poducto"] == subopcion_update and len(detalles) > 1 :
                                gotoxy(2,33+linea);print("Seguro que desea eliminar el producto (s)")
                                gotoxy(2,33+linea);valido = validar.solo_letras("Error solo letras",34,33)
                                if valido == "si" or valido =="s":
                                    del detalles[i]
                                    subtotal, discount, iva, total = sale.cal(detalles)
                                    invoce["subtotal"] = round(subtotal, 2)
                                    invoce["descuento"] = round(discount, 2)
                                    invoce["iva"] = round(iva, 2)
                                    invoce["total"] = round(total, 2)
                                    print("Producto eliminado.")
                                    json_file.save(invoices)
                                    producto_encontrado = True
                                    break
                                else:
                                    print("Accion Cancelada")
                        
                        if not producto_encontrado:
                            print("Producto no encontrado.")
                        if bandera:
                          print("Quiere seguir eliminando productos? Presione 'f' para continuar o cualquier otra tecla para salir: ")
                          respuesta = validar.solo_letras("Error solo letras",106,35+linea)
                          if respuesta.lower() != 'f':
                              bandera = False
            elif opcion == '8':
                print("Operación de actualización cancelada.")
            else:
                print("Opción no válida.")
            
            
        else:
            print(f"No se encontró la factura con el número {invoice_number}.")
        
        input("Presione una tecla para continuar...")
        
    def delete(self):
        validar = Valida()
        print('\033c', end='')
        gotoxy(2,1);print(green_color+"█"*90)
        gotoxy(2,2);print("██"+" "*34+"Eliminación de Factura"+" "*35+"██")
        gotoxy(2,4);print("Ingrese el número de factura a eliminar: ")
        gotoxy(2,4);invoice_number = validar.solo_numeros("Error: Solo Numeros",44,4)
        invoice_num = int(invoice_number)
        json_file = JsonFile(path+'/archivos/invoices.json')
        invoices = json_file.read()
        busqueda = json_file.find("factura",invoice_num)
        if busqueda:
            invoce = busqueda[0]
            print(f"Impresion de la Factura#{invoice_num}")
            gotoxy(13,6);print("----------------------------- Factura Encontrada ---------------------------")
            gotoxy(13,7);print("Factura    ")
            gotoxy(26,7);print("Fecha      ")
            gotoxy(39,7);print("Cliente    ")
            gotoxy(52,7);print("Subtotal   ")
            gotoxy(65,7);print("Descuento  ")
            gotoxy(78,7);print("IVA        ")
            gotoxy(91,7);print("Total  ")
            gotoxy(13,8);print(f"¦¦{invoce['factura']}  ¦¦")
            gotoxy(26,8);print(f"¦¦{invoce['Fecha']}    ¦¦")
            gotoxy(39,8);print(f"¦¦{invoce['cliente']}  ¦¦")
            gotoxy(52,8);print(f"¦¦{invoce['subtotal']} ¦¦")
            gotoxy(65,8);print(f"¦¦{invoce['descuento']}¦¦")
            gotoxy(78,8);print(f"¦¦{invoce['iva']}      ¦¦")
            gotoxy(91,8);print(f"¦¦{invoce['total']}    ¦¦")
            gotoxy(13,10);print("---------------------------------- Detalles -------------------------------")
            detalles=busqueda[0]["detalle"]
            gotoxy(13,11);print("Producto   ")
            gotoxy(26,11);print("Precio     ")
            gotoxy(39,11);print("Cantidad   ")
            linea=0
            for x in detalles:
                gotoxy(13,12+linea);print(x["poducto"])
                gotoxy(26,12+linea);print(x["precio"])
                gotoxy(39,12+linea);print(x["cantidad"])
                linea+=1
            gotoxy(13,13+linea);print("-"*75)   
            time.sleep(3)
            gotoxy(13,14+linea);print("¿Seguro que deseas eliminar esta factura (si/no)?: ")
            confirmacion = validar.solo_letras("Error: Solo Letras",64,14+linea).lower()
            if confirmacion == 'si' or confirmacion == "s":
                invoices.remove(busqueda[0])
                json_file.save(invoices)
                print("✔✔ Factura eliminada exitosamente. ✔✔")
            else:
                print("Operación de eliminación cancelada.")
        else:
          print(f"No se encontró la factura con el número {invoice_number}.")

    def consult(self):
        validar = Valida()
        print('\033c', end='')
        gotoxy(2,1);print(green_color+"█"*90)
        gotoxy(2,2);print("██"+" "*34+"Consulta de Venta"+" "*35+"██")
        gotoxy(2,4);invoice= input("Ingrese el Numero de la Factura  ").strip()
        borrarPantalla()
        print('\033c', end='')
        gotoxy(2,1);print(green_color+"█"*90)
        gotoxy(2,2);print("██"+" "*34+"Consulta de Venta"+" "*35+"██")
        if invoice.isdigit():
            invoice = int(invoice)
            json_file = JsonFile(path+'/archivos/invoices.json')
            invoices = json_file.find("factura",invoice)
            gotoxy(1,5);print("-"*109)
            gotoxy(38, 5);print(f"Impresion de la Factura # {invoice}")
            if invoices:
                factura_info = invoices[0]
                gotoxy(2, 7); print("Factura")
                gotoxy(15, 7); print("Fecha")
                gotoxy(30, 7); print("Cliente")
                gotoxy(45, 7); print("Subtotal")
                gotoxy(60, 7); print("Descuento")
                gotoxy(75, 7); print("IVA")
                gotoxy(90, 7); print("Total")
                gotoxy(5, 8); print(f"{factura_info['factura']}")
                gotoxy(13, 8); print(f"{factura_info['Fecha']}")
                gotoxy(28, 8); print(f"{factura_info['cliente']}")
                gotoxy(46, 8); print(f"{factura_info['subtotal']}")
                gotoxy(62, 8); print(f"{factura_info['descuento']}")
                gotoxy(75, 8); print(f"{factura_info['iva']}")
                gotoxy(90, 8); print(f"{factura_info['total']}")
                gotoxy(1,10);print("-"*109)
                gotoxy(28, 12);print(f"Impresion de los detalles")
                detalles = factura_info['detalle']
                gotoxy(13,14);print("Producto   ")
                gotoxy(26,14);print("Precio     ")
                gotoxy(39,14);print("Cantidad   ")
                linea=0
                for x in detalles:
                    gotoxy(13,15+linea);print(x["poducto"])
                    gotoxy(26,15+linea);print(x["precio"])
                    gotoxy(39,15+linea);print(x["cantidad"])
                    linea+=1
                gotoxy(1,17+linea);print("-"*109)
        else:    
            json_file = JsonFile(path+'/archivos/invoices.json')
            invoices = json_file.read()
            print("Consulta de Facturas")
            for fac in invoices:
                print(f"{fac['factura']}   {fac['Fecha']}   {fac['cliente']}   {fac['total']}")
            
            suma = reduce(lambda total, invoice: round(total+ invoice["total"],2), 
            invoices,0)
            totales_map = list(map(lambda invoice: invoice["total"], invoices))
            total_client = list(filter(lambda invoice: invoice["cliente"] == "Dayanna Vera", invoices))

            max_invoice = max(totales_map)
            min_invoice = min(totales_map)
            tot_invoices = sum(totales_map)
            print("filter cliente: ",total_client)
            print(f"              map Facturas:{totales_map}")
            print(f"              max Factura:{max_invoice}")
            print(f"              min Factura:{min_invoice}")
            print(f"              sum Factura:{tot_invoices}")
            print(f"              reduce Facturas:{suma}")
        gotoxy(2,40);x=input("presione una tecla para continuar...")   

#producto con más stock
#producto con menos stock
#clientes con más compras
#clientes con menos compras
#ventas - facturas con mayor y menor valor

def ConsultasGenerales():
    borrarPantalla()
    
    # PRODUCTO CON MÁS STOCK
    json_file = JsonFile(path+'/archivos/products.json') 
    # se lee el json productos
    products = json_file.read() 
    # se crea un list comprehension con 2 for, el primero usará enumerate 
    # para identificar el index de los productos con mayor stock
    # el segundo for se usa para encontrar la mayor cantidad de stock de algún producto
    # entonces se hace una validación para únicamente guardar los productos que
    # tengan la mayor cantidad de stock (se guardan los diccionarios de cada producto del json products)
    products_major_stock = [products[idx] for idx, stock in enumerate(products) if stock["stock"] == max([x['stock'] for x in products])]
    print("\033[1;32m**"*50)
    gotoxy(40,2);print("PRODUCTO CON MAYOR STOCK") 
    gotoxy(13,4);print("Producto   ")
    gotoxy(26,4);print("Precio     ")
    gotoxy(39,4);print("Stock   ")
    linea=0
    for x in products_major_stock:
        gotoxy(13,6+linea);print(x["descripcion"])
        gotoxy(26,6+linea);print(x["precio"])
        gotoxy(39,6+linea);print(x["stock"])
        linea+=1
    print("*"*100)    
    
    # PRODUCTO CON MENOS STOCK
    # básicamente es lo mismo de arriba pero en el segundo for se guarda la menor cantidad de stock
    products_menor_stock = [products[idx] for idx, stock in enumerate(products) if stock["stock"] == min([x['stock'] for x in products])]
    print("\033[1;35m*****"*20)
    gotoxy(40,8+linea);print("PRODUCTO CON MENOR STOCK")
    gotoxy(13,10+linea);print("Producto   ")
    gotoxy(26,10+linea);print("Precio     ")
    gotoxy(39,10+linea);print("Stock   ")
    for x in products_menor_stock:
        gotoxy(13,12+linea);print(x["descripcion"])
        gotoxy(26,12+linea);print(x["precio"])
        gotoxy(39,12+linea);print(x["stock"])
        linea+=1
    print("*****"*20)    
    
    # CLIENTES CON MÁS FACTURAS
    # se identifican y se leen los json de facturas y clientes
    json_file_invoices = JsonFile(path+'/archivos/invoices.json')
    json_file_clients = JsonFile(path+'/archivos/clients.json')
    invoices = json_file_invoices.read()
    
    # se crea un set/conjunto con el dni de todos los clientes de las facturas
    clients = set([x['dni'] for x in invoices]) 
    
    # se crea un list comprehension que tendrá diccionarios
    # se realiza un ciclo for de los dni y los guardamos en un diccionario
    # también se guarda el número de facturas que existen con ese dni, usando el .find de los json
    dicionary_clients = [{'dni': client, 'facturas': len(json_file_invoices.find('dni', client))} for client in clients] 
    
    # se crea un list comprehension usando la misma lógica que se usó para obtener los
    # productos con mayor y menor stock. El primer for recorrerá los diccionarios de todos los clientes 
    # el segundo for usará la función max() para encontrar la cantidad máxima de facturas
    # luego usando una validación, se guardan los diccionarios de los clientes que tengan la mayor
    # cantidad de facturas.
    clients_invoices = [x for x in dicionary_clients if x['facturas'] == max([x['facturas'] for x in dicionary_clients])]

    # se valida si existe más de un elemento en la lista clients_invoices
    # se usará el .find de los json para buscar a los clientes en el json de clientes
    # si se encuentra el dni, lo presenta.
    # si existe más de 1 elemento en la lista, se hará lo mismo pero realizando un ciclo for
    print("\033[1;33m**"*50)
    gotoxy(40,14+linea);print("CLIENTES CON MÁS FACTURAS")
    if len(clients_invoices) == 1:
        client_found = json_file_clients.find('dni', clients_invoices[0]['dni'])
        gotoxy(13,16+linea);print("DNI   ")
        gotoxy(26,16+linea);print("Nombre     ")
        gotoxy(39,16+linea);print("Apellido   ")
        gotoxy(52,16+linea);print("Numero de Facturas")
        if client_found:
            for x in client_found:
                gotoxy(13,18+linea);print(x["dni"])
                gotoxy(26,18+linea);print(x["nombre"])
                gotoxy(39,18+linea);print(x["apellido"])
                gotoxy(52,18+linea);print(clients_invoices[0]['facturas'])
                linea+=1
    elif len(clients_invoices) > 1 :
        gotoxy(13,16+linea);print("DNI   ")
        gotoxy(26,16+linea);print("Nombre     ")
        gotoxy(39,16+linea);print("Apellido   ")
        gotoxy(52,16+linea);print("Numero de Facturas")
        for x in clients_invoices:
            client_found = json_file_clients.find('dni', x['dni'])
            if client_found:
                for x in client_found:
                    gotoxy(13,18+linea);print(x["dni"])
                    gotoxy(26,18+linea);print(x["nombre"])
                    gotoxy(39,18+linea);print(x["apellido"])
                    gotoxy(52,18+linea);print(clients_invoices[0]['facturas'])
                linea+=1
    print("**"*50)
    
    # FACTURAS CON MAYOR VALOR
    invoices_higher_value = [x for x in invoices if x['total'] == max([x['total'] for x in invoices])]
    print("\033[1;32m**"*50)
    gotoxy(40, 20+linea);print("FACTURAS CON MAYOR VALOR")
    if invoices_higher_value: 
        gotoxy(2, 22+linea); print("Factura")
        gotoxy(15,22+linea); print("Fecha")
        gotoxy(30,22+linea); print("Cliente")
        gotoxy(45,22+linea); print("Subtotal")
        gotoxy(60,22+linea); print("Descuento")
        gotoxy(75, 22+linea); print("IVA")
        gotoxy(90,22+linea); print("Total")
        for x ,f in enumerate(invoices_higher_value):
            factura_info = invoices_higher_value[x]
            gotoxy(5, 24+linea); print(f"{factura_info['factura']}")
            gotoxy(13, 24+linea); print(f"{factura_info['Fecha']}")
            gotoxy(28, 24+linea); print(f"{factura_info['cliente']}")
            gotoxy(46, 24+linea); print(f"{factura_info['subtotal']}")
            gotoxy(62, 24+linea); print(f"{factura_info['descuento']}")
            gotoxy(75, 24+linea); print(f"{factura_info['iva']}")
            gotoxy(90, 24+linea); print(f"{factura_info['total']}")
            linea+=1
    print("**"*50)
    
    
    # FACTURAS CON MENOR VALOR
    invoices_lower_value = [x for x in invoices if x['total'] == min([x['total'] for x in invoices])]
    print("\033[1;35m**"*50)
    gotoxy(40, 27+linea);print("FACTURAS CON MENOR VALOR")
    if invoices_lower_value: 
        gotoxy(2, 29+linea); print("Factura")
        gotoxy(15,29+linea); print("Fecha")
        gotoxy(30,29+linea); print("Cliente")
        gotoxy(45,29+linea); print("Subtotal")
        gotoxy(60,29+linea); print("Descuento")
        gotoxy(75, 29+linea); print("IVA")
        gotoxy(90,29+linea); print("Total")
        for x ,f in enumerate(invoices_lower_value):
            factura_info = invoices_lower_value[x]
            gotoxy(5, 31+linea); print(f"{factura_info['factura']}")
            gotoxy(13, 31+linea); print(f"{factura_info['Fecha']}")
            gotoxy(28, 31+linea); print(f"{factura_info['cliente']}")
            gotoxy(46, 31+linea); print(f"{factura_info['subtotal']}")
            gotoxy(62, 31+linea); print(f"{factura_info['descuento']}")
            gotoxy(75, 31+linea); print(f"{factura_info['iva']}")
            gotoxy(90, 31+linea); print(f"{factura_info['total']}")
            linea+=1
    print("**"*50)



#Menu Proceso Principal
opc=''
while opc !='5':
    borrarPantalla()
    menu_main = Menu("Menu Facturacion",["1) Clientes","2) Productos","3) Ventas","4) Consultas Generales", "5) Salir"],20,10)
    opc = menu_main.menu()
    if opc == "1":
        opc1 = ''
        while opc1 !='5':
            borrarPantalla()
            clients = CrudClients()
            menu_clients = Menu("Menu Cientes",["1) Ingresar","2) Actualizar","3) Eliminar","4) Consultar","5) Salir"],20,10)
            opc1 = menu_clients.menu()
            if opc1 == "1":
                clients.create()
            elif opc1 == "2":
                clients.update()
            elif opc1 == "3":
                clients.delete()
            elif opc1 == "4":
                clients.consult()
            elif opc1 == "5":
                print("Regresando al menu Clientes...")
            # time.sleep(2)
    elif opc == "2":
        opc2 = ''
        while opc2 !='5':
            borrarPantalla()
            products = CrudProducts()
            menu_products = Menu("Menu Productos",["1) Ingresar","2) Actualizar","3) Eliminar","4) Consultar","5) Salir"],20,10)
            opc2 = menu_products.menu()
            if opc2 == "1":
                products.create()
            elif opc2 == "2":
                products.update()
            elif opc2 == "3":
                products.delete()
            elif opc2 == "4":
                products.consult()
            elif opc2 == "5":
                print("Regresando al menu Clientes...")
    elif opc == "3":
        opc3 =''
        while opc3 !='5':
            borrarPantalla()
            sales = CrudSales()
            menu_sales = Menu("Menu Ventas",["1) Registro Venta","2) Consultar","3) Modificar","4) Eliminar","5) Salir"],20,10)
            opc3 = menu_sales.menu()
            if opc3 == "1":
                sales.create()
                time.sleep(2)
            elif opc3 == "2":
                sales.consult()
                time.sleep(2)
            elif opc3 == "3":
                sales.update()
            elif opc3 == "4":
                sales.delete()
            elif opc3 == "5":
                print("Regresando al menu Clientes...")
    elif opc == "4":
        ConsultasGenerales()
        input("Presione una tecla para salir...")


#producto con más stock
#producto con menos stock
#clientes con más compras
#clientes con menos compras
#ventas - facturas con mayor y menor valor

    print("Regresando al menu Principal...")
    # time.sleep(2)

borrarPantalla()
input("Presione una tecla para salir...")
borrarPantalla()