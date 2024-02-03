class TreeNode:
    def __init__(self):
        # Inicializa um nó com uma lista de chaves e uma lista de filhos.
        self.keys = []
        self.children = []

class Tree234:
    def __init__(self):
        # Inicializa a árvore 2-3-4 com uma raiz vazia.
        self.root = None
    def insert(self, data):
        # Insere um valor na árvore 2-3-4.
        if self.root is None:
            # Se a árvore estiver vazia, cria a raiz.
            self.root = TreeNode()
        if data in self.percorre_em_ordem():
            # Verifica se o valor já está na árvore para evitar duplicação de chaves.
            return
        if len(self.root.keys) == 3:
            # verifica a necessidade de split.
            new_root = TreeNode()
            new_root.children.append(self.root)
            self.split(new_root, 0)
            self.root = new_root
        self.insert_recursiva(self.root, data)

    def insert_recursiva(self, node, data):
        # Função auxiliar para inserção recursiva.
        i = 0
        while i < len(node.keys) and data > node.keys[i]:
            i += 1
        if len(node.children) == 0:
            # Se o nó é uma folha, insere o valor nas chaves do nó.
            node.keys.insert(i, data)
        else:
            if i < len(node.keys) and data == node.keys[i]:
                # Evita inserção de chaves duplicadas.
                return
            if len(node.children) > i and len(node.children[i].keys) == 3:
                # Se o filho tem três chaves, realiza o split.
                self.split(node, i)
                if data > node.keys[i]:
                    i += 1
            if len(node.children) > i:
                self.insert_recursiva(node.children[i], data)

    def split(self, node, child_index):
        # Função para o split propriamente dito.
        child = node.children[child_index]
        middle_key = child.keys[1]
        node.keys.insert(child_index, middle_key)

        new_node = TreeNode()
        new_node.keys.append(child.keys[2])

        if child.children:  # Move os filhos, se existirem.
            new_node.children.append(child.children[2])
            new_node.children.append(child.children[3])
            child.children = child.children[:2]

        node.children.insert(child_index + 1, new_node)
        child.keys = [child.keys[0]]  # Mantém a primeira chave no filho.

    def remocaao(self, data):
        # função para remoção de chaves da árvore.
        if not self.root:
            return "A árvore está vazia."

        if data not in self.percorre_em_ordem():
            # Verifica se o valor está presente na árvore.
            return f"{data} não está na árvore."

        self.remocaao_recursiva(self.root, data)

        if len(self.root.keys) == 0:
            if len(self.root.children) == 1:
                # Se a raiz não tem chaves e tem apenas um filho, a raiz é substituída pelo filho.
                self.root = self.root.children[0]
            else:
                # Se não, a raiz fica vazia.
                self.root = None
        return f"{data} removido com sucesso."
    
    def remocaao_recursiva(self, node, data):
        # Função auxiliar para remoção recursiva.
        i = 0
        while i < len(node.keys) and data > node.keys[i]:
            i += 1

        if i < len(node.keys) and data == node.keys[i]:
            if len(node.children) == 0:
                # Se o nó é uma folha, remove a chave.
                del node.keys[i]
            else:
                if len(node.children[i + 1].children) > 0:
                    # Se o próximo filho tem filhos, encontra o valor mínimo no filho à direita.
                    node.keys[i] = self.get_min(node.children[i + 1])
                    self.remocaao_recursiva(node.children[i + 1], node.keys[i])
                else:
                    # Caso contrário, encontra o valor máximo no filho à esquerda.
                    node.keys[i] = self.get_max(node.children[i])
                    self.remocaao_recursiva(node.children[i], node.keys[i])
        elif len(node.children) > i:
            if len(node.children[i].keys) < 2:
                # verifica se o filho tenha pelo menos duas chaves.
                self.verif_filho(node, i)
            self.remocaao_recursiva(node.children[i], data)

    def verif_filho(self, node, child_index):
        # verifica se um filho tem pelo menos duas chaves.
        child = node.children[child_index]
        if child_index > 0 and len(node.children[child_index - 1].keys) > 1:
            self.rotacaao_direita(node, child_index - 1)
        elif child_index < len(node.children) - 1 and len(node.children[child_index + 1].keys) > 1:
            self.rotacaao_esquerda(node, child_index)
        else:
            if child_index > 0:
                self.merge(node, child_index - 1)
            else:
                self.merge(node, child_index)

    def rotacaao_esquerda(self, node, child_index):
        # Realiza uma rotação à esquerda em um filho.
        left_child = node.children[child_index]
        right_child = node.children[child_index + 1]
        left_child.keys.append(node.keys[child_index])
        node.keys[child_index] = right_child.keys[0]
        del right_child.keys[0]
        if right_child.children:
            left_child.children.append(right_child.children[0])
            del right_child.children[0]

    def rotacaao_direita(self, node, child_index):
        # Realiza uma rotação à direita em um filho.
        right_child = node.children[child_index + 1]
        left_child = node.children[child_index]
        right_child.keys.insert(0, node.keys[child_index])
        node.keys[child_index] = left_child.keys[-1]
        del left_child.keys[-1]
        if right_child.children:
            right_child.children.insert(0, left_child.children[-1])
            del left_child.children[-1]

    def merge(self, node, child_index):
        # Realiza a fusão de um filho com seu vizinho.
        left_child = node.children[child_index]
        right_child = node.children[child_index + 1]
        left_child.keys.append(node.keys[child_index])
        left_child.keys.extend(right_child.keys)
        left_child.children.extend(right_child.children)
        del node.keys[child_index]
        del node.children[child_index + 1]

    def get_min(self, node):
        # Encontra o valor mínimo na árvore.
        while len(node.children) > 0:
            node = node.children[0]
        return node.keys[0]
    
    def get_max(self, node):
        # Encontra o valor máximo na árvore.
        while len(node.children) > 0:
            node = node.children[-1]
        return node.keys[-1]
    
    def percorre_em_ordem(self):
        # Realiza uma travessia in-order da árvore e retorna as chaves em ordem.
        return self._percorre_em_ordem_rec(self.root)
    
    def _percorre_em_ordem_rec(self, node):
        if not node:
            return []

        result = []
        for i in range(len(node.keys)):
            if len(node.children) > i:
                result.extend(self._percorre_em_ordem_rec(node.children[i]))
            result.append(node.keys[i])
        if node.children:
            result.extend(self._percorre_em_ordem_rec(node.children[-1]))
        return result
    
    def percorre_em_ordem(self):
        # Realiza uma travessia pré-ordem da árvore e retorna as chaves em ordem.
        return self._percorre_em_ordem_rec(self.root)
    
    def _percorre_em_ordem_rec(self, node):
        # Função auxiliar para a travessia pré-ordem.
        if not node:
            return []

        result = [node.keys[i] for i in range(len(node.keys))]
        for child in node.children:
            result.extend(self._percorre_em_ordem_rec(child))
        return result
    
    def percorre_pos_ordem(self):
        # Realiza uma travessia pós-ordem da árvore e retorna as chaves em ordem.
        return self._percorre_pos_ordem_rec(self.root)
    
    def _percorre_pos_ordem_rec(self, node):
       # Função auxiliar para a travessia pós-ordem.
        if not node:
            return []

        result = []
        for i in range(len(node.keys)):
            if len(node.children) > i:
                result.extend(self._percorre_pos_ordem_rec(node.children[i]))
        if node.children:
            result.extend(self._percorre_pos_ordem_rec(node.children[-1]))
        result.extend(node.keys)
        return result
    
    def __str__(self):
        # Retorna uma representação de string da árvore para impressão.
        if not self.root:
            return "Árvore Vazia"

        lines = []
        level = [self.root]
        while level:
            next_level = []
            line = []
            for node in level:
                if node.children:
                    next_level.extend(node.children)
                line.append("|".join(map(str, node.keys)))
            lines.append(" | ".join(line))
            level = next_level

        return "\n".join(lines)
    
def main():
    tree = Tree234()

    while True:
        print("\nMenu:")
        print("1. Inserir uma chave")
        print("2. remover uma chave")
        print("3. Imprimir a árvore")
        print("4. Imprimir em Pré-ordem")
        print("5. Imprimir em Pós-ordem")
        print("6. Sair")

        choice = input("Informe a sua escolha: ")

        if choice == '1':
            data = int(input("Informe a chave para inserir na árvore: "))
            tree.insert(data)
            print(tree)

        elif choice == '2':
            data = int(input("Informe a chave para remoção: "))
            print(tree.remocaao(data))
            print(tree)

        elif choice == '3':
            print(tree)

        elif choice == '4':
            print("Pré-ordem:", tree.percorre_em_ordem())

        elif choice == '5':
            print("Pós-ordem:", tree.percorre_pos_ordem())

        elif choice == '6':
            break

        else:
            print("Escolha inválida!")

if __name__ == '__main__':
    main()
