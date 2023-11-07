import sqlite3
from datetime import datetime


def criar_tabela():
    conn = sqlite3.connect("tarefas.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tarefas (
            id INTEGER PRIMARY KEY,
            nome TEXT NOT NULL,
            data_adicao DATE NOT NULL,
            data_vencimento DATE NOT NULL,
            descricao TEXT,
            prioridade INTEGER
        )
    """)

    conn.commit()
    conn.close()


def adicionar_tarefa():
    conn = sqlite3.connect("tarefas.db")
    cursor = conn.cursor()

    nome = input("Nome da tarefa: ")
    data_adicao = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    data_vencimento = input("Data de vencimento: ")
    descricao = input("Descrição da tarefa: ")

    while True:
        prioridade = input("Prioridade (0 a 5): ")
        if prioridade.isdigit() and 0 <= int(prioridade) <= 5:
            prioridade = int(prioridade)
            break
        else:
            print("A prioridade deve estar no intervalo de 0 a 5. Tente novamente.")

    cursor.execute("""
        INSERT INTO tarefas (nome, data_adicao, data_vencimento, descricao, prioridade)
        VALUES (?, ?, ?, ?, ?)
    """, (nome, data_adicao, data_vencimento, descricao, prioridade))

    conn.commit()
    conn.close()


def get_tarefas():
    conn = sqlite3.connect("tarefas.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM tarefas
        ORDER BY prioridade DESC
    """)

    tarefas = cursor.fetchall()

    conn.close()

    return tarefas


def excluir_tarefa(id_tarefa):
    conn = sqlite3.connect("tarefas.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM tarefas WHERE id = ?", (id_tarefa,))

    conn.commit()
    conn.close()


def atualizar_tarefa(nome_tarefa, nova_data_vencimento, nova_descricao, nova_prioridade):
    conn = sqlite3.connect("tarefas.db")
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE tarefas
        SET data_vencimento = ?,
            descricao = ?,
            prioridade = ?,
            data_adicao = ?
        WHERE id = ?
    """, (nova_data_vencimento, nova_descricao, nova_prioridade,
          datetime.now().strftime('%Y-%m-%d %H:%M:%S'), nome_tarefa))

    conn.commit()
    conn.close()


def main():
    while True:
        print("\nEscolha uma opção:")
        print("1 - Adicionar Tarefa")
        print("2 - Listar Tarefas")
        print("3 - Excluir Tarefa")
        print("4 - Atualizar Tarefa")
        print("5 - Sobre")
        print("0 - Sair")
        opcao = input("Opção: ")

        if opcao == "1":
            adicionar_tarefa()
            print("Tarefa adicionada com sucesso.")
        elif opcao == "2":
            tarefas = get_tarefas()
            if not tarefas:
                print("Nenhuma tarefa encontrada.")
            else:
                print("\nLista de Tarefas:")
                for tarefa in tarefas:
                    print(f"Nome da tarefa: {tarefa[1]} || Prioridade: {tarefa[5]}."
                          f"\nDescrição: {tarefa[4]}"
                          f"\nAdicionada em {tarefa[2]}\n"
                          f"Vence em {tarefa[3]}\n"
                          f"------------------------------------------------------------")
        elif opcao == "3":
            tarefas = get_tarefas()
            if not tarefas:
                print("Nenhuma tarefa encontrada.")
            else:
                print("\nEscolha a tarefa para excluir:")
                for i, tarefa in enumerate(tarefas):
                    print(f"{i+1} - {tarefa[1]}\n"
                          f"Descrição: {tarefa[4]}\n"
                          f"------------------------------------------------------------")
                opcao_excluir = int(input("Opção: ")) - 1
                if opcao_excluir == "0":
                    print("Operação de exclusão cancelada.")
                if 0 <= opcao_excluir < len(tarefas):
                    id_tarefa = tarefas[opcao_excluir][0]
                    excluir_tarefa(id_tarefa)
                    print(f"Tarefa excluída com sucesso.")
                else:
                    print("Opção inválida.")
        elif opcao == "4":
            tarefas = get_tarefas()
            if not tarefas:
                print("Nenhuma tarefa encontrada.")
            else:
                print("Escolha a tarefa para atualizar (ou pressione 0 para voltar):")
                for i, tarefa in enumerate(tarefas):
                    print(f"{i + 1} - {tarefa[1]}")
                opcao_atualizar = input("Opção: ")
                if opcao_atualizar == "0":
                    print("Operação de atualização cancelada.")
                elif opcao_atualizar.isdigit():
                    opcao_atualizar = int(opcao_atualizar) - 1
                    if 0 <= opcao_atualizar < len(tarefas):
                        nome_tarefa = tarefas[opcao_atualizar][0]
                        nova_data_vencimento = input("Nova Data de Vencimento: ")
                        nova_descricao = input("Nova Descrição: ")
                        nova_prioridade = int(input("Nova Prioridade (de 0 a 5): "))
                        atualizar_tarefa(nome_tarefa, nova_data_vencimento, nova_descricao, nova_prioridade)
                        print(f"Tarefa '{nome_tarefa}' atualizada com sucesso.")
                    else:
                        print("Opção inválida.")
                else:
                    print("Opção inválida.")
        elif opcao == "5":
            print("\nDesenvolvido por Heitor Pavani Nolla como Projeto Final do Program Match!\n")
            print("Este é o Projeto 2: Aplicativo de Gerenciamento de Tarefas com Verificação de Prioridade")
            print("Permite que o usuário cadastre, visualize, atualize e delete tarefas")
            print("O programa conta com persistência de dados, feita por meio do banco de dados SQLite\n")
            print("Atualizado pela última vez em 09/11/2023. Obrigado Mastertech e IBM pela oportunidade")
        elif opcao == "0":
            break
        else:
            print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
    main()
