'''    def novo(self, tabela, data: dict):
        colunas = ", ".join(data.keys()) # n,  nome,  
        colunas_ref = ", ".join(["?" for i in len(data)])
        inst = f"INSERT INTO {tabela} ({colunas}) VALUES ({colunas_ref})"
        self.database_link.execute(inst, *data.values())
'''