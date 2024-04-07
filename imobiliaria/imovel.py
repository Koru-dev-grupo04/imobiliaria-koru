import sqlite3

class Imovel:
    def __init__(self, descricao, endereco, valor, cidade, tipo, imagem, id=None):
        self.id = id
        self.descricao = descricao
        self.endereco = endereco
        self.valor = valor
        self.cidade = cidade
        self.tipo = tipo
        self.imagem = imagem

    def to_dict(self):
        return {
            "id" : self.id,
            "descricao" : self.descricao,
            "endereco" : self.endereco,
            "valor" : self.valor,
            "cidade" : self.cidade,
            "tipo" : self.tipo,
            "imagem" : self.imagem
        }

    def save(self, db_connection:sqlite3.Connection):
        if self.id == None:
            query = '''
        INSERT INTO IMOVEIS (
        IMAGEM, TIPO, CIDADE, ENDERECO, DESCRICAO, VALOR
        ) VALUES (?, ?, ?, ?, ?, ?)
    '''
            cursor = db_connection.cursor()
            cursor.execute(query,(
                self.imagem,
                self.tipo,
                self.cidade,
                self.endereco,
                self.descricao,
                self.valor
                ))
            self.id = cursor.lastrowid
        else:
            query = '''
        UPDATE IMOVEIS 
        SET 
        IMAGEM = ?, TIPO = ?, CIDADE = ?, ENDERECO = ?, DESCRICAO = ?, VALOR = ?
        WHERE ID = ?
    '''
            db_connection.execute(query,(
                self.imagem,
                self.tipo,
                self.cidade,
                self.endereco,
                self.descricao,
                self.valor,
                self.id
            ))
        db_connection.commit()
        db_connection.close()

    def delete(self,db:sqlite3.Connection):
        query = '''
        DELETE FROM IMOVEIS WHERE ID = ?
    '''
        cursor = db.cursor()
        cursor.execute(query, (self.id,))
        db.commit()
        


    @staticmethod
    def get_by_id(id:int, db:sqlite3.Connection):
        query = '''
        SELECT * FROM IMOVEIS WHERE ID = ?
'''
        cursor = db.cursor()
        result = db.execute(query, (id,)).fetchone()
        if result:
            return Imovel(
                id = result[0],
                descricao = result[1],
                endereco = result[2],
                valor = result[3],
                cidade = result[4],
                tipo = result[5],
                imagem = result[6]
                )
        else:
            return None
        
    @staticmethod
    def get_all(db:sqlite3.Connection):
        query = '''
            SELECT * FROM IMOVEIS
    '''
        cursor = db.cursor()
        results = cursor.execute(query).fetchall()
        imoveis = []
        for result in results:
            imoveis.append(Imovel(
                id = result[0],
                descricao = result[1],
                endereco = result[2],
                valor = result[3],
                cidade = result[4],
                tipo = result[5],
                imagem = result[6]
                ).to_dict())
        return imoveis
