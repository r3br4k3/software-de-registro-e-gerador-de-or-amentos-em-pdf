import tkinter as tk
from tkinter import ttk, messagebox
import xml.etree.ElementTree as ET
from datetime import datetime
import os
import getpass

def load_or_create_xml(filename='clients.xml'):
    if not os.path.exists(filename):
        root = ET.Element("Clients")
        tree = ET.ElementTree(root)
        tree.write(filename)
    return ET.parse(filename)

def get_next_id(root):
    ids = [int(client.find('ID').text) for client in root.findall('Client') if client.find('ID') is not None]
    return str(max(ids) + 1) if ids else '1'

def add_or_update_client(cpf, name, street, neighborhood, city, phone1, phone2, description, observation, filename='clients.xml'):
    tree = load_or_create_xml(filename)
    root = tree.getroot()
    found = False
    
    for client in root.findall('Client'):
        if client.find('CPF').text == cpf:
            client.find('Name').text = name
            client.find('Street').text = street
            client.find('Neighborhood').text = neighborhood
            client.find('City').text = city
            client.find('Phone1').text = phone1
            client.find('Phone2').text = phone2
            client.find('Description').text = description
            client.find('Observation').text = observation
            client.find('RegisteredBy').text = getpass.getuser()
            client.find('LastModified').text = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            found = True
            break
    
    if not found:
        client = ET.SubElement(root, "Client")
        ET.SubElement(client, "ID").text = get_next_id(root)
        ET.SubElement(client, "CPF").text = cpf
        ET.SubElement(client, "Name").text = name
        ET.SubElement(client, "Street").text = street
        ET.SubElement(client, "Neighborhood").text = neighborhood
        ET.SubElement(client, "City").text = city
        ET.SubElement(client, "Phone1").text = phone1
        ET.SubElement(client, "Phone2").text = phone2
        ET.SubElement(client, "Description").text = description
        ET.SubElement(client, "Observation").text = observation
        ET.SubElement(client, "RegisteredBy").text = getpass.getuser()
        ET.SubElement(client, "LastModified").text = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    tree.write(filename)

def get_client_by_id(client_id, filename='clients.xml'):
    xml_data = load_or_create_xml(filename)
    root = xml_data.getroot()
    for client in root.findall('Client'):
        if client.find('ID').text == client_id:
            return {
                "cpf": client.find('CPF').text,
                "name": client.find('Name').text,
                "street": client.find('Street').text,
                "neighborhood": client.find('Neighborhood').text,
                "city": client.find('City').text,
                "phone1": client.find('Phone1').text,
                "phone2": client.find('Phone2').text,
                "description": client.find('Description').text,
            }
    return None

def show_clients_window():
    window = tk.Toplevel()
    window.title("Lista de Clientes")

    search_var = tk.StringVar()
    search_entry = ttk.Entry(window, textvariable=search_var)
    search_entry.pack(fill='x', padx=10, pady=5)

    tree = ttk.Treeview(window, columns=('ID', 'CPF', 'Name', 'Street', 'Neighborhood', 'City', 'Phone1', 'Phone2'), show='headings')
    
    # Definindo a largura das colunas
    tree.heading('ID', text='ID')
    tree.column('ID', width=50, stretch=False)  # Ajusta a largura para 50 pixels

    tree.heading('CPF', text='CPF')
    tree.column('CPF', width=120, stretch=False)  # Ajusta a largura para 120 pixels

    tree.heading('Name', text='Nome')
    tree.column('Name', width=150, stretch=False)  # Ajusta a largura para 150 pixels

    tree.heading('Street', text='Rua')
    tree.column('Street', width=200, stretch=False)  # Ajusta a largura para 200 pixels

    tree.heading('Neighborhood', text='Bairro')
    tree.column('Neighborhood', width=150, stretch=False)  # Ajusta a largura para 150 pixels

    tree.heading('City', text='Cidade')
    tree.column('City', width=120, stretch=False)  # Ajusta a largura para 120 pixels

    tree.heading('Phone1', text='Telefone 1')
    tree.column('Phone1', width=100, stretch=False)  # Ajusta a largura para 100 pixels

    tree.heading('Phone2', text='Telefone 2')
    tree.column('Phone2', width=100, stretch=False)  # Ajusta a largura para 100 pixels

    tree.pack(fill='both', expand=True)

    def update_search(*args):
        search_text = search_var.get().lower()
        for item in tree.get_children():
            tree.delete(item)
        xml_data = load_or_create_xml()
        root = xml_data.getroot()
        clients = [(int(client.find('ID').text), client) for client in root.findall('Client') if client.find('ID') is not None]
        clients.sort()  # Ordena por ID
        for id_num, client in clients:
            if not search_text or search_text in client.find('Name').text.lower() or search_text in client.find('CPF').text:
                tree.insert("", 'end', values=(client.find('ID').text, client.find('CPF').text,
                                               client.find('Name').text, client.find('Street').text,
                                               client.find('Neighborhood').text, client.find('City').text,
                                               client.find('Phone1').text, client.find('Phone2').text))
    search_var.trace('w', update_search)
    update_search()  # Carrega os dados inicialmente


def create_budget_window():
    window = tk.Toplevel()
    window.title("Criar Orçamento")

    # Campos de entrada para informações do cliente
    ttk.Label(window, text="ID do Cliente:").grid(row=0, column=0, padx=10, pady=5, sticky='w')
    entry_client_id = ttk.Entry(window)
    entry_client_id.grid(row=0, column=1, sticky='ew')

    ttk.Label(window, text="Nome do Cliente:").grid(row=1, column=0, padx=10, pady=5, sticky='w')
    entry_client_name = ttk.Entry(window)
    entry_client_name.grid(row=1, column=1, sticky='ew')

    ttk.Label(window, text="CPF do Cliente:").grid(row=2, column=0, padx=10, pady=5, sticky='w')
    entry_client_cpf = ttk.Entry(window)
    entry_client_cpf.grid(row=2, column=1, sticky='ew')

    ttk.Label(window, text="Rua:").grid(row=3, column=0, padx=10, pady=5, sticky='w')
    entry_client_street = ttk.Entry(window)
    entry_client_street.grid(row=3, column=1, sticky='ew')

    ttk.Label(window, text="Bairro:").grid(row=4, column=0, padx=10, pady=5, sticky='w')
    entry_client_neighborhood = ttk.Entry(window)
    entry_client_neighborhood.grid(row=4, column=1, sticky='ew')

    ttk.Label(window, text="Cidade:").grid(row=5, column=0, padx=10, pady=5, sticky='w')
    entry_client_city = ttk.Entry(window)
    entry_client_city.grid(row=5, column=1, sticky='ew')

    ttk.Label(window, text="Telefone 1:").grid(row=6, column=0, padx=10, pady=5, sticky='w')
    entry_client_phone1 = ttk.Entry(window)
    entry_client_phone1.grid(row=6, column=1, sticky='ew')

    ttk.Label(window, text="Telefone 2 (opcional):").grid(row=7, column=0, padx=10, pady=5, sticky='w')
    entry_client_phone2 = ttk.Entry(window)
    entry_client_phone2.grid(row=7, column=1, sticky='ew')

    ttk.Label(window, text="Descrição:").grid(row=8, column=0, padx=10, pady=5, sticky='w')
    entry_client_description = tk.Text(window, height=4)
    entry_client_description.grid(row=8, column=1, sticky='ew')

    # Campos de entrada para itens do orçamento
    item_frame = ttk.Frame(window)
    item_frame.grid(row=9, column=0, columnspan=2, padx=10, pady=5, sticky='ew')

    ttk.Label(item_frame, text="Quantidade:").grid(row=0, column=0, padx=5)
    entry_quantity = ttk.Entry(item_frame)
    entry_quantity.grid(row=0, column=1, padx=5)

    ttk.Label(item_frame, text="Descrição do Serviço:").grid(row=0, column=2, padx=5)
    entry_service_description = ttk.Entry(item_frame)
    entry_service_description.grid(row=0, column=3, padx=5)

    ttk.Label(item_frame, text="Valor:").grid(row=0, column=4, padx=5)
    entry_value = ttk.Entry(item_frame)
    entry_value.grid(row=0, column=5, padx=5)

    # Adicionar mais linhas
    def add_item_row():
        row_count = len(item_frame.grid_slaves()) // 6
        ttk.Label(item_frame, text="Quantidade:").grid(row=row_count, column=0, padx=5)
        ttk.Entry(item_frame).grid(row=row_count, column=1, padx=5)
        ttk.Label(item_frame, text="Descrição do Serviço:").grid(row=row_count, column=2, padx=5)
        ttk.Entry(item_frame).grid(row=row_count, column=3, padx=5)
        ttk.Label(item_frame, text="Valor:").grid(row=row_count, column=4, padx=5)
        ttk.Entry(item_frame).grid(row=row_count, column=5, padx=5)

    ttk.Button(window, text="Adicionar Item", command=add_item_row).grid(row=10, column=1, pady=10)

    def load_client_by_id():
        client_id = entry_client_id.get()
        if not client_id:
            messagebox.showerror("Erro", "Por favor, insira um ID para buscar.")
            return
        
        client_data = get_client_by_id(client_id)
        if client_data:
            entry_client_name.delete(0, tk.END)
            entry_client_name.insert(0, client_data["name"])
            entry_client_cpf.delete(0, tk.END)
            entry_client_cpf.insert(0, client_data["cpf"])
            entry_client_street.delete(0, tk.END)
            entry_client_street.insert(0, client_data["street"])
            entry_client_neighborhood.delete(0, tk.END)
            entry_client_neighborhood.insert(0, client_data["neighborhood"])
            entry_client_city.delete(0, tk.END)
            entry_client_city.insert(0, client_data["city"])
            entry_client_phone1.delete(0, tk.END)
            entry_client_phone1.insert(0, client_data["phone1"])
            entry_client_phone2.delete(0, tk.END)
            entry_client_phone2.insert(0, client_data["phone2"])
            entry_client_description.delete("1.0", tk.END)
            entry_client_description.insert("1.0", client_data["description"])
        else:
            messagebox.showerror("Erro", "Cliente não encontrado.")

    ttk.Button(window, text="Carregar Cliente", command=load_client_by_id).grid(row=0, column=2, padx=10, pady=5)

    def save_budget():
        client_id = entry_client_id.get()
        client_name = entry_client_name.get()
        client_cpf = entry_client_cpf.get()
        items = []
        
        # Coletar dados de cada linha de item
        for child in item_frame.grid_slaves():
            if isinstance(child, ttk.Entry):
                items.append(child.get())
        
        if client_id and client_name and client_cpf:
            # Aqui você pode adicionar lógica para salvar o orçamento em um arquivo ou banco de dados
            messagebox.showinfo("Sucesso", "Orçamento criado com sucesso!")
            window.destroy()
        else:
            messagebox.showerror("Erro", "Preencha todos os campos obrigatórios.")

    ttk.Button(window, text="Salvar Orçamento", command=save_budget).grid(row=11, column=1, pady=10)

def add_edit_client_window():
    window = tk.Toplevel()
    window.title("Adicionar/Editar Cliente")

    ttk.Label(window, text="Pesquisar CPF:").grid(row=0, column=0, padx=10, pady=5, sticky='w')
    search_var = tk.StringVar()
    search_entry = ttk.Entry(window, textvariable=search_var)
    search_entry.grid(row=0, column=1, sticky='ew')

    def load_client():
        cpf = search_var.get()
        if not cpf:
            messagebox.showerror("Erro", "Por favor, insira um CPF para buscar.")
            return
        
        xml_data = load_or_create_xml()
        root = xml_data.getroot()
        for client in root.findall('Client'):
            if client.find('CPF').text == cpf:
                entry_cpf.delete(0, tk.END)
                entry_cpf.insert(0, client.find('CPF').text)
                entry_name.delete(0, tk.END)
                entry_name.insert(0, client.find('Name').text)
                entry_street.delete(0, tk.END)
                entry_street.insert(0, client.find('Street').text)
                entry_neighborhood.delete(0, tk.END)
                entry_neighborhood.insert(0, client.find('Neighborhood').text)
                entry_city.delete(0, tk.END)
                entry_city.insert(0, client.find('City').text)
                entry_phone1.delete(0, tk.END)
                entry_phone1.insert(0, client.find('Phone1').text)
                entry_phone2.delete(0, tk.END)
                entry_phone2.insert(0, client.find('Phone2').text)
                text_description.delete("1.0", tk.END)
                text_description.insert("1.0", client.find('Description').text)
                text_observation.delete("1.0", tk.END)
                text_observation.insert("1.0", client.find('Observation').text)
                return
        
        messagebox.showerror("Erro", "Cliente não encontrado.")

    ttk.Button(window, text="Carregar Cliente", command=load_client).grid(row=0, column=2, padx=10, pady=5)

    ttk.Label(window, text="CPF:").grid(row=1, column=0, padx=10, pady=5, sticky='w')
    entry_cpf = ttk.Entry(window)
    entry_cpf.grid(row=1, column=1, sticky='ew')

    ttk.Label(window, text="Nome:").grid(row=2, column=0, padx=10, pady=5, sticky='w')
    entry_name = ttk.Entry(window)
    entry_name.grid(row=2, column=1, sticky='ew')

    ttk.Label(window, text="Rua:").grid(row=3, column=0, padx=10, pady=5, sticky='w')
    entry_street = ttk.Entry(window)
    entry_street.grid(row=3, column=1, sticky='ew')

    ttk.Label(window, text="Bairro:").grid(row=4, column=0, padx=10, pady=5, sticky='w')
    entry_neighborhood = ttk.Entry(window)
    entry_neighborhood.grid(row=4, column=1, sticky='ew')

    ttk.Label(window, text="Cidade:").grid(row=5, column=0, padx=10, pady=5, sticky='w')
    entry_city = ttk.Entry(window)
    entry_city.grid(row=5, column=1, sticky='ew')

    ttk.Label(window, text="Telefone 1:").grid(row=6, column=0, padx=10, pady=5, sticky='w')
    entry_phone1 = ttk.Entry(window)
    entry_phone1.grid(row=6, column=1, sticky='ew')

    ttk.Label(window, text="Telefone 2 (opcional):").grid(row=7, column=0, padx=10, pady=5, sticky='w')
    entry_phone2 = ttk.Entry(window)
    entry_phone2.grid(row=7, column=1, sticky='ew')

    ttk.Label(window, text="Descrição:").grid(row=8, column=0, padx=10, pady=5, sticky='w')
    text_description = tk.Text(window, height=4)
    text_description.grid(row=8, column=1, sticky='ew')

    ttk.Label(window, text="Observação:").grid(row=9, column=0, padx=10, pady=5, sticky='w')
    text_observation = tk.Text(window, height=4)
    text_observation.grid(row=9, column=1, sticky='ew')

    def save_client():
        cpf = entry_cpf.get()
        name = entry_name.get()
        street = entry_street.get()
        neighborhood = entry_neighborhood.get()
        city = entry_city.get()
        phone1 = entry_phone1.get()
        phone2 = entry_phone2.get()
        description = text_description.get("1.0", "end-1c")
        observation = text_observation.get("1.0", "end-1c")
        
        if cpf and name and street and neighborhood and city and phone1:
            add_or_update_client(cpf, name, street, neighborhood, city, phone1, phone2, description, observation)
            messagebox.showinfo("Sucesso", "Cliente salvo/atualizado com sucesso!")
            window.destroy()
        else:
            messagebox.showerror("Erro", "Preencha todos os campos obrigatórios.")

    ttk.Button(window, text="Salvar Cliente", command=save_client).grid(row=10, column=1, pady=10, sticky='ew')

    def delete_client():
        cpf = entry_cpf.get()
        if cpf and messagebox.askyesno("Confirmar", "Você tem certeza que deseja deletar este cliente?"):
            if delete_client_from_xml(cpf):
                messagebox.showinfo("Sucesso", "Cliente deletado com sucesso!")
                window.destroy()  # Fecha a janela após deletar
            else:
                messagebox.showerror("Erro", "Cliente não encontrado.")

    ttk.Button(window, text="Deletar Cliente", command=delete_client).grid(row=11, column=1, pady=10, sticky='ew')

    # Configurações de responsividade
    window.grid_columnconfigure(0, weight=1)
    window.grid_columnconfigure(1, weight=2)

def main_window():
    root = tk.Tk()
    root.title("Sistema de Gestão de Clientes")

    ttk.Button(root, text="Clientes", command=show_clients_window).pack(fill='x', padx=50, pady=20)
    ttk.Button(root, text="Adicionar/Editar Cliente", command=add_edit_client_window).pack(fill='x', padx=50, pady=20)
    ttk.Button(root, text="Criar Orçamento", command=create_budget_window).pack(fill='x', padx=50, pady=20)

    root.mainloop()

if __name__ == "__main__":
    main_window()
