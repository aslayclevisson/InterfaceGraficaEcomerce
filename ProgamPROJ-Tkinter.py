'''
Universidade Federal de Pernambuco - (UFPE) - (https://www.ufpe.br/)
Centro de Informática (CIn) - (https://www2.cin.ufpe.br/site/index.php)
Graduando - Sistemas de Informação
Programação 1 - IF968

Autor: Aslay Clevisson Soares Santos - (acss3)
E-mail: acss3@cin.ufpe.br
Data: 21-11-2019
Copyright(c) 2019 Aslay Clevisson Soares Santos
'''
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import csv
from datetime import datetime

dicio_user={}
#abertura dos arquivos necessários para armazenar os dados
usu = open('dados_usuarios_cad.csv', mode='a', encoding='utf-8', newline='')
serv = open('dados_servicos.csv', mode='a', encoding='utf-8', newline='')
compras_usu = open('dados_de_compras_usu.csv', mode='a', encoding='utf-8', newline='')

#implementa no dic, qualquer valor no banco de dados, de forma mais atualizada
with open('dados_usuarios_cad.csv','r') as BD:
            leitura = csv.reader(BD)         
            for linha in leitura:
                dicio_user[linha[2]]=(linha[0],[linha[1], linha[4]],linha[3])

dicio_admin = {'admin':('admin')}
class Programa():

    def verifLogin(self):
        '''
        verifica se um usuário está de acordo com os critérios de login
        se houver algo incorreto, será notificado.
        '''
        login=str(self.login.get())
        senha=str(self.senha.get())
        self.nivel=1
        #verificar se o login e senha está no dicio ADMIN, se estiver, ele da uma nível ao usuário e autentica
        for usu in dicio_admin.items():
            if login == usu[0] and senha == usu[1]:
                messagebox.showinfo('login','Autenticado.')
                self.janela.destroy()
                self.nivel=3
                self.admin()
        else:
            with open('dados_usuarios_cad.csv','r') as entrada:
                leitura = csv.reader(entrada)
                for x in leitura:
                    #pega do banco de dados, a senha criptografada do usuário e descriptografa essa senha para fazer a análise de login e senha
                    aux=x[4].split(',')
                    aux_int=[int(j) for j in aux]
                    descripto=''.join([str(chr(x**1079 % 1073)) for x in aux_int])
                    #verifica se o login e senha está no banco de dados e compara se é nível 1 ou nível 2 e autentica o usuário
                    if senha == descripto and x[3].lower() == login:
                        if x[5] == '1':
                            self.label_conf_login['text']='Ok.'
                            messagebox.showinfo('login','Autenticado.')
                            self.dadosUsu = x
                            self.janela.destroy()
                            self.nivel=1
                            self.addcarrinho=[]
                            self.usuarioNormal()
                     
                        if x[5] == '2':
                            self.label_conf_login['text']='Ok.'
                            messagebox.showinfo('login','Autenticado.')
                            self.dadosSubAdmin = x
                            self.nivel=2
                            self.janela.destroy()
                            self.subAdmin()
                    self.label_conf_login['text']='Login ou senha errados, tente novamente.'

###########################################################################################################################
    def subAdmin(self):
        '''
        Abre a janela de opções de nível 2 e mostra uma Treeview dos agendamentos realizados
        e que estão em um banco de dados
        mostra opções de cadastro de servico, cadastro de usuario, servicos e agendamentos
        '''
        self.janela = Tk ()
        self.janela.title('SubADMIN')
        self.janela['bg']='#B8D6F0'
        self.janela.geometry('+500+250')

        self.tree = ttk.Treeview(self.janela,selectmode='browse',column=('column1','column2','column3'), show='headings')
        
        self.tree.column('column1', width=100,minwidth=200,stretch=NO)
        self.tree.heading('#1', text='Nome')

        self.tree.column('column2', width=100,minwidth=200,stretch=NO)
        self.tree.heading('#2', text='Data') 

        self.tree.column('column3', width=80,minwidth=200,stretch=NO)
        self.tree.heading('#3', text='Hora')


        self.tree.grid(row=2, column=2,padx=4,pady=4,rowspan=6,columnspan=2)
        
        #os botões carregam comandos ao serem clicados
        Button(self.janela, text='Cadastrar novo serviço', width=20, command=self.janeCadServico, bg='#22467D', fg='white').grid(row=1,column=1,padx=4,pady=4)
        Button(self.janela, text='Cadastros Usuários', width=20, command=self.vizualizarCadUsu, bg='#22467D', fg='white').grid(row=2,column=1,padx=4,pady=4)
        Button(self.janela, text='Serviços', width=20, command=self.vizualizarServicos, bg='#22467D', fg='white').grid(row=3,column=1,padx=4,pady=4)
        Button(self.janela, text='Agendamentos', width=20, bg='#22467D', fg='white').grid(row=1,column=2, columnspan=2, sticky=W+E,padx=4,pady=4)
        Button(self.janela, text='Deslogar', width=20,command=self.logoff, bg='#22467D', fg='white').grid(row=8,column=3, sticky=E,padx=4,pady=4)
        self.janela.mainloop()

                            
    def usuarioNormal(self):
        '''
        Abre a janela de opções de nível 1
        opões de compra e agendamento, além das informações do usuário
        '''
        #Evoca uma janela e adiciona nosvos elementos a ela ao longo das linhas
        self.janela = Tk ()
        self.janela['bg']='#B8D6F0'
        self.janela.title('Usuário')
        self.janela.geometry('+500+250')

        #os botões carregam comandos ao serem clicados
        Button(self.janela, text='Produtos/Serviços', width=20,command=self.painelItens, bg='#22467D', fg='white').grid(row=1,column=1,padx=4,pady=4)
        Button(self.janela, text='Agendar serviço', width=20, bg='#22467D', fg='white').grid(row=2,column=1,padx=4,pady=4)
        Button(self.janela, text='Informações de conta', width=20, bg='#22467D', fg='white', command=self.informacoesDeConta).grid(row=1,column=2,padx=4,pady=4)
        Button(self.janela, text='Deslogar', width=20,command=self.logoff, bg='#22467D', fg='white').grid(row=2,column=2,padx=4,pady=4)

        self.janela.mainloop()

    def painelItens(self):
        '''
        Abre uma nova janela com uma Treeview de informações dos 
        serviços que estão disponíveis para compra pelo usuário de nível 1
        oções expostas: Buscador de produto, add produto no carrinho, carrinho, atualizar a janela
        '''
        self.janela.destroy()
        #Evoca uma janela e adiciona nosvos elementos a ela ao longo das linhas
        self.janela = Tk ()
        self.janela['bg']='#B8D6F0'
        self.janela.title('Produtos')
        self.janela.geometry('+500+250')

        #evoca uma tabela para itens
        self.treeServ = ttk.Treeview(self.janela,selectmode='browse',column=('column1','column2','column3'), show='headings')
        
        self.treeServ.column('column1', width=150,minwidth=200,stretch=NO)
        self.treeServ.heading('#1', text='Produto')

        self.treeServ.column('column2', width=150,minwidth=200,stretch=NO)
        self.treeServ.heading('#2', text='Grupo') 

        self.treeServ.column('column3', width=100,minwidth=200,stretch=NO)
        self.treeServ.heading('#3', text='Preço R$  ') 

        self.treeServ.grid(row=0, column=0,padx=4,pady=4,rowspan=4, columnspan=3)

        #botões de comandos
        Button(self.janela, text='Buscar produto', width=20, command=self.buscarProduto, bg='#22467D', fg='white').grid(row=0,column=4, sticky=S,padx=5,pady=2)
        Button(self.janela, text='Adicionar ao carrinho', width=20, bg='#22467D', fg='white', command=self.adicionarCarrinho).grid(row=1,column=4,sticky=S,padx=2,pady=2)
        Button(self.janela, text='Carrinho', width=20, bg='#22467D', fg='white', command=self.carrinhoCompras).grid(row=2,column=4,sticky=S,padx=2,pady=2)        
        Button(self.janela, text='Atualizar guia', width=20,command=self.painelItens, bg='#22467D', fg='white').grid(row=3,column=4,sticky=S,padx=5,pady=2)
        Button(self.janela, text='Voltar', width=10, command=self.atualizarInformacoes, bg='#22467D', fg='white').grid(row=4,column=0,padx=2,pady=2, sticky=W)
        
        #armazenador das linhas que que são recolhidas do Arq.CSV. Esses dados são guardados para serem adicionados na Treeview
        armazenadorDeLinha=[]
        #leitura de arquivo CSV
        with open('dados_servicos.csv','r') as bancoD:
                leitura = csv.reader(bancoD)
                for linha in leitura:                    
                    armazenadorDeLinha=linha
                    #adiciona o valor guardado em armazenadorDeLinha, na tabela Treeview
                    self.treeServ.insert("", END, values=armazenadorDeLinha, iid=linha[3], tag='1')

        self.janela.mainloop()
    

    def janeCadServico(self):
        '''
        Evoca uma janela para ser realizada o cadastro do usuário, recebendo entradas dos dados escritos pelo usuário
        '''
        self.janela.destroy()
        #Evoca uma janela e adiciona nosvos elementos a ela ao longo das linhas
        self.janela = Tk()
        self.janela['bg']='#B8D6F0'
        self.janela.resizable(False,False)
        self.janela.title('Cad. Serviço')
        self.janela.geometry('300x450+500+250')
        #escrita da janela(Label) e entradas para os usuários(Entry)
        Label(self.janela, text='Nome do produto:',bg='#B8D6F0').grid(row=1, column=1, sticky=E, padx=4, pady=4)
        self.servico = Entry(self.janela)
        self.servico.grid(row=1, column=2,columnspan=2, padx=4, pady=4)

        Label(self.janela, text='Grupo produto:',bg='#B8D6F0').grid(row=2, column=1, sticky=E, padx=4, pady=4)
        self.grupo = Entry(self.janela)
        self.grupo.grid(row=2, column=2, columnspan=2, padx=4, pady=4)

        Label(self.janela, text='Preço do produto:',bg='#B8D6F0').grid(row=3, column=1, sticky=E, padx=4, pady=4)
        self.preco_servico = Entry(self.janela)
        self.preco_servico.grid(row=3, column=2, columnspan=2, padx=4, pady=4)

        #botões de comando
        Button(self.janela, text='Confirmar',command=self.cadServico, bg='#22467D', fg='white').grid(row=4, column=3, padx=4, pady=4)
        Button(self.janela, text='Voltar', command=self.atualizarInformacoes, bg='#22467D', fg='white').grid(row=4, column=2, padx=4, pady=4)


    def cadServico(self):
        '''
        Implementa um Identificador do produto e escreve todos os dados 
        que são escritos em relação a produtos, no banco de dados
        '''   

        #as variávels servico,grupo, preco..., recebem os valores que foram escritos nas entradas de usuários/produtos e armazeram esses dados  
        servico=str(self.servico.get())
        grupo=str(self.grupo.get())
        preco_servico=str(self.preco_servico.get())

        id_produto=0
        datahora_modificacao=datetime.now()
        #abre um banco de dados dos serviços
        with open('dados_servicos.csv', mode='a', encoding='utf-8', newline='') as servicos:
            #faz uma leitura dos dados já existentes no banco de dados do serviço
            with open('dados_servicos.csv', mode='r', encoding='utf-8', newline='') as leituServ:
                leitura = csv.reader(leituServ)
                armaz=[]
                #implementação do ID do produto
                for x in leitura:
                    armaz.append(x)
                aux=0
                id_produto=0
                if armaz != []:
                    for y in armaz:
                        if int(y[3])>aux:
                            aux=int(y[3])
                    id_produto=aux+1
                else:
                    if armaz == []:
                        id_produto+=1
            
            #indica a escrita no arquivo
            writer = csv.writer(servicos)
            
            #escreve todos os dados recebidos pelas variáveis serv., grup., preco. e Id do produto       
            writer.writerow([servico,grupo,preco_servico,id_produto])
            if self.nivel == 2:
                arq = open('registro.txt','a')
                arq.write(f'O Subadmin {self.dadosSubAdmin[0]}, com CPF {self.dadosSubAdmin[2]}, adicionou um novo produto no sistema, com o nome {servico} e no valor de {preco_servico}R$ Unid.  no dia {datahora_modificacao.day}/{datahora_modificacao.month}/{datahora_modificacao.year} às {datahora_modificacao.hour}:{datahora_modificacao.minute}:{datahora_modificacao.second}.\n\n')
                arq.close()
            messagebox.showinfo('Cadastro','Cadastro de produto realizado.')
        self.janela.destroy()
        if self.nivel == 3:
            self.admin()
        else:
            self.subAdmin()

    
    def vizualizarServicos(self):
        '''
        Evoca uma janela para vizualizar todos os produtos cadastrados no banco de dados(Janela dispoível para ADMIN e SUBADMIN)
        Opções como remover/limpar tudo, atualizar produto e busca dos produtos, estão presentes na janela 
        '''
        self.janela.destroy()
        #Evoca uma janela e adiciona nosvos elementos a ela ao longo das linhas
        self.janela = Tk()  
        self.janela.resizable(False,False)
        self.janela['bg']='#B8D6F0'
        self.janela.title('Serviços cadastrados')
        self.janela.geometry('+500+250')

        #treeview(tabela) dos produtos já cadastrados
        self.treeServ = ttk.Treeview(self.janela,selectmode='browse',column=('column1','column2','column3'), show='headings')
        
        self.treeServ.column('column1', width=150,minwidth=200,stretch=NO)
        self.treeServ.heading('#1', text='Produto')

        self.treeServ.column('column2', width=150,minwidth=200,stretch=NO)
        self.treeServ.heading('#2', text='Grupo') 

        self.treeServ.column('column3', width=100,minwidth=200,stretch=NO)
        self.treeServ.heading('#3', text='Preço R$  ') 

        self.treeServ.grid(row=0, column=0,padx=4,pady=4,rowspan=4, columnspan=3)

        #botões de comandos
        Button(self.janela, text='Buscar produto', width=20, command=self.buscarProduto, bg='#22467D', fg='white').grid(row=0,column=4,sticky=S,padx=5,pady=2)
        Button(self.janela, text='Remover produto', width=20,command=self.removerServ, bg='#22467D', fg='white').grid(row=1,column=4,sticky=S,padx=2,pady=2)
        Button(self.janela, text='Atualizar produto', width=20,command=self.janelaAtualizarProduto, bg='#22467D', fg='white').grid(row=2,sticky=S,column=4,padx=5,pady=2)

        if self.nivel == 3:
            Button(self.janela, text='Limpar produtos', width=20,command=self.limpaServ, bg='#22467D', fg='white').grid(row=3,column=4,sticky=S,padx=2,pady=2)

        volta=Button(self.janela, text='Voltar', width=10, command=self.atualizarInformacoes, bg='#22467D', fg='white').grid(row=5,column=0,sticky=W,padx=2,pady=2)

        armazenadorDeLinha=[]
        #abre o banco de dados e o lê para adicionar os elementos na treeview
        with open('dados_servicos.csv','r') as bancoD:
                leitura = csv.reader(bancoD)
                for linha in leitura:                    
                    armazenadorDeLinha=linha
                    self.treeServ.insert("", END, values=armazenadorDeLinha, iid=linha[3], tag='1')

        self.janela.mainloop()

        
    def vizualizarCadUsu(self):
        '''
        Evoca janela de informações(Vizível apenas pelo ADMIN e SUBADMIN), como os usuários cadastrados já no sistema(banco D.) e botões de comando para:
        a remoção, upgrade de nível/downgrade e limpar todos cadastros
        '''
        self.janela.destroy()
        #Evoca uma janela e adiciona nosvos elementos a ela ao longo das linhas
        self.janela = Tk()  
        self.janela['bg']='#B8D6F0'
        self.janela.resizable(False,False)
        self.janela.title('Cadastro Usuários')
        self.janela.geometry('+500+250')

        #treeview(tabela) dos usuários já cadastrados
        self.tree = ttk.Treeview(self.janela,selectmode='browse',column=('column1','column2','column3','column4','column5','column6','column7'), show='headings')
        
        self.tree.column('column1', width=100,minwidth=200,stretch=NO)
        self.tree.heading('#1', text='NOME')

        self.tree.column('column2', width=100,minwidth=200,stretch=NO)
        self.tree.heading('#2', text='ENDEREÇO') 

        self.tree.column('column3', width=80,minwidth=200,stretch=NO)
        self.tree.heading('#3', text='CPF')

        self.tree.column('column4', width=100,minwidth=200,stretch=NO)
        self.tree.heading('#4', text='LOGIN')

        self.tree.column('column5', width=100,minwidth=200,stretch=NO)
        self.tree.heading('#5', text='CÓDIGO')

        self.tree.column('column6', width=40,minwidth=200,stretch=NO)
        self.tree.heading('#6', text='NÍVEL')

        self.tree.column('column7', width=45,minwidth=200,stretch=NO)
        self.tree.heading('#7', text='ID')

        self.tree.grid(row=0, column=0,padx=4,pady=4,rowspan=5, columnspan=6)

        #botões de comando
        Button(self.janela, text='Buscar Usuário', width=20,command=self.buscarUsuario, bg='#22467D', fg='white').grid(row=0,column=7,sticky=S,padx=2,pady=2)
        if self.nivel == 3:
            Button(self.janela, text='Remover Cadastro', width=20,command=self.removerCad, bg='#22467D', fg='white').grid(row=1,column=7,sticky=S,padx=2,pady=2)
            Button(self.janela, text='Up Cadastro', width=20,command=self.upCad, bg='#22467D', fg='white').grid(row=2,column=7,sticky=S,padx=5,pady=2)
            Button(self.janela, text='Down Cadastro', width=20,command=self.downCad, bg='#22467D', fg='white').grid(row=3,column=7,sticky=S,padx=5,pady=2)
            Button(self.janela, text='Limpar cadastros', width=20,command=self.limpaCads, bg='#22467D', fg='white').grid(row=4,column=7,sticky=S,padx=2,pady=2)

        volta=Button(self.janela, text='Voltar', width=10, command=self.atualizarInformacoes, bg='#22467D', fg='white').grid(row=5,column=0, sticky=W,padx=2,pady=2)

        armazenadorDeLinha=[]
        #abre o banco de dados e o lê para adicionar os elementos na treeview
        with open('dados_usuarios_cad.csv','r') as bancoD:
                leitura = csv.reader(bancoD)
                for linha in leitura:                    
                    armazenadorDeLinha=linha
                    self.tree.insert("", END, values=armazenadorDeLinha, iid=linha[6], tag='1')
                    #armazenadorDeLinha.clear()

        self.janela.mainloop()

      
    def atualizarInformacoes(self):
        '''
        função para verificar o nível do usuário e abrir a janela correspondente, quando apertar no botão de comando
        "voltar".
        '''
        self.janela.destroy()
        if self.nivel == 2:
            self.subAdmin()
        elif self.nivel == 3:
            #
            with open('dados_usuarios_cad.csv','r') as bancoD:
                leitura = csv.reader(bancoD)
                arq_regist = open('informacoes_usu.txt','a')
                for linha in leitura:                    
                    arq_regist.write(f'{linha[2]}\t{linha[0]}\t{linha[1]}\t{linha[3]}\t{linha[4]}\n\n')
                arq_regist.close()
    
            self.admin()
        elif self.nivel == 1:
            self.usuarioNormal()
   


    def admin(self):
        '''
        Evoca o painel do administrador, com botões de comando compatíveis com o cargo, ou seja,
        acesso a todas informações armazenadas pelo programa
        '''
        self.janela = Tk ()
        self.janela.title('ADMIN')
        self.janela.geometry('+500+250')
        self.janela['bg']='#B8D6F0'
        self.tree = ttk.Treeview(self.janela,selectmode='browse',column=('column1','column2','column3','column4','column5','column6','column7','column8'), show='headings')
        
        #treeview de agendamentos
        self.tree.column('column1', width=100,minwidth=200,stretch=NO)
        self.tree.heading('#1', text='Nome')

        self.tree.column('column2', width=100,minwidth=200,stretch=NO)
        self.tree.heading('#2', text='CPF') 

        self.tree.column('column3', width=80,minwidth=200,stretch=NO)
        self.tree.heading('#3', text='Produto')

        self.tree.column('column4', width=100,minwidth=200,stretch=NO)
        self.tree.heading('#4', text='Grupo')

        self.tree.column('column5', width=100,minwidth=200,stretch=NO)
        self.tree.heading('#5', text='Preço R$')

        self.tree.column('column6', width=100,minwidth=200,stretch=NO)
        self.tree.heading('#6', text='Qntd.')

        self.tree.column('column7', width=100,minwidth=200,stretch=NO)
        self.tree.heading('#7', text='Data de compra')

        self.tree.column('column8', width=100,minwidth=200,stretch=NO)
        self.tree.heading('#8', text='Hora de compra')

        self.tree.grid(row=2, column=0,padx=4,pady=4,rowspan=8,columnspan=8)        

        #botões de comando
        Button(self.janela, text='Cadastrar novo produto', width=20, command=self.janeCadServico,bg='#22467D', fg='white').grid(row=1,column=1,sticky=W,padx=4,pady=4)
        Button(self.janela, text='Cadastros Usuários', width=20, command=self.vizualizarCadUsu,bg='#22467D', fg='white').grid(row=1,column=2,sticky=W,padx=4,pady=4)
        Button(self.janela, text='Atualizar', width=20,command=self.atualizarInformacoes, bg='#22467D', fg='white').grid(row=10,column=0, sticky=W+E, columnspan=2,padx=4,pady=4)
        Button(self.janela, text='Produtos', width=20, command=self.vizualizarServicos,bg='#22467D', fg='white').grid(row=1,column=3,sticky=W,padx=4,pady=4)
        Button(self.janela, text='Agendamentos', width=20,bg='#22467D', fg='white').grid(row=1,column=4,sticky=W,padx=4,pady=4)
        Button(self.janela, text='Deslogar', width=20,command=self.logoff, bg='#22467D', fg='white').grid(row=1,column=5,sticky=S,padx=4,pady=4)
        
        with open('dados_de_compras_usu.csv','r') as bancoD_compras:
            leitura = csv.reader(bancoD_compras)
            for linha in leitura:                    
                #armazenadorDeLinha=linha
                self.tree.insert("", END, values=linha, tag='1')

        self.janela.mainloop()

    
    def logoff(self):
        '''
        Desconecta o usuário e evoca a janela inicial de login
        '''
        #caixa de mensagem True/False
        if messagebox.askokcancel('Desconectar','Deseja desconectar a conta?'):
            self.janela.destroy()
            self.__init__()

       
    def cadastro(self):
        '''
        Recolhe os dados dispoonibilizados nas entradas de cadastro e armazena seus 
        dados com a senha criptografada no banco de dados e em um arquivo

        Adicional - implementa ID ao usuário
        '''
        arq_regist = open('dados_cad.txt','a')
        #as variáveis abaixo, armazenam as informações fornecidas nas entradas de cadastro do usuário
        nome = str(self.nome.get().title())
        endereco = str(self.endereco.get().title())
        cpf=str(self.cpf.get())
        criar_login = str(self.login.get())
        criar_senha = str(self.senha.get())

    ####criptografia
        cripto = ','.join([str(ord(x)**71 % 1073) for x in criar_senha])
        dicio_user[criar_login] = [criar_senha, (cpf, nome), endereco]
        #escreve as variáveis com as informações fornecidas e escrevem num arquivo TXT
        arq_regist.write(f'{cpf}\t{nome}\t{endereco}\t{criar_login}\t{cripto}\n\n')
        arq_regist.close()
        
        #Abre um arquivo CSV em modo leitura
        with open('dados_usuarios_cad.csv', mode='r', encoding='utf-8', newline='') as linhas:
            leitura = csv.reader(linhas)
            armaz=[]
            #adiciona um ID ao usuário
            for x in leitura:
                armaz.append(x)
            aux=0
            id_usuario=0
            if armaz != []:
                for y in armaz:
                    if int(y[6])>aux:
                        aux=int(y[6])
                id_usuario=aux+1
            else:
                if armaz == []:
                    id_usuario+=1

        #abre o arquivo csv e adiciona os novos elementos ao banco de dados
        with open('dados_usuarios_cad.csv', mode='a', encoding='utf-8', newline='') as csv_file:
            fieldnames = ['Nome', 'Endereco', 'CPF', 'Login', 'Codigo','Nível','ID']
            writer = csv.writer(csv_file)         
            writer.writerow([nome,endereco,cpf,criar_login,cripto,1,id_usuario])
                            
        messagebox.showinfo('Cadastro Usuário','Cadastro concluído com sucesso.')
        self.janela.destroy()
        #Label(self.janela,command=log)
        #evoca a janela inicial de login
        self.__init__()


    def cad(self):
        '''
        Abre janela de cadastro e recebe todos os inputs dos usuários que irão fazer o cadastro, tais como:
        Endereço, cpf, login, senha, nome e etc.
        '''
        self.janela.destroy()
        self.janela = Tk ()
        self.janela['bg']='#B8D6F0'
        self.janela.title('Cadastro')
        self.janela.geometry('375x400+500+250')
        
        #descreve a relação entre cada entrada, ou seja, descreve as caixas de login, senha, cpf e etc...
        Label(self.janela,text='Nome:',bg='#B8D6F0').grid(row=0, column=0, sticky=E, padx = 4, pady = 4)
        self.nome = Entry(self.janela)
        self.nome.grid(row=0,column=1, columnspan=2, padx = 4, pady = 4)
        
        Label(self.janela,text='Endereço:',bg='#B8D6F0').grid(row=1, column=0, sticky=E, padx = 4, pady = 4)
        self.endereco = Entry(self.janela)
        self.endereco.grid(row=1,column=1,columnspan=2, padx = 4, pady = 4)

        Label(self.janela,text='CPF:',bg='#B8D6F0').grid(row=2, column=0, sticky=E, padx = 4, pady = 4)
        self.cpf = Entry(self.janela)
        self.cpf.grid(row=2,column=1,columnspan=2, padx = 4, pady = 4)

        Label(self.janela,text='Seu login:',bg='#B8D6F0').grid(row=3, column=0, sticky=E, padx = 4, pady = 4)
        self.login = Entry(self.janela)
        self.login.grid(row=3,column=1,columnspan=2, padx = 4, pady = 4)
        self.resp = Label(self.janela,text=' ',bg='#B8D6F0')
        self.resp.grid(row=3, column=3, padx = 4, pady = 4)

        Label(self.janela,text='Sua senha:',bg='#B8D6F0').grid(row=4, column=0, sticky=E, padx = 4, pady = 4)
        self.senha = Entry(self.janela)
        self.senha.grid(row=4,column=1, columnspan=2, padx = 4, pady = 4)
        self.verificSenha = Label(self.janela,text=' ',bg='#B8D6F0')
        self.verificSenha.grid(row=4, column=3, padx = 4, pady = 4)

        self.janela.resizable(False,False)
        
        Button(self.janela, text='Confirmar', bg='orange',command=self.verLog).grid(row=5, column=2, columnspan=1, padx = 4, pady = 4)
        Button(self.janela, text='Voltar', bg='orange',command=self.voltarLog).grid(row=5, column=1, columnspan=1, padx = 4, pady = 4)
        
        self.janela.mainloop()


    def voltarLog(self):
        '''
        Destroi a janela e volta pra tela inicial de login
        '''
        self.janela.destroy()
        self.__init__()

        
    def verLog(self):
        '''
        Verifica os critérios para a criação de login. Se o login dado no cadastro, já existe no banco de dados, 
        se ele está apto a ter mais de 4 caracteres, se foi dado alguma informação ou se ele está apto à criação
        '''
        armazenador=[]
        with open('dados_usuarios_cad.csv','r') as entrada:
            leitura = csv.reader(entrada)
            #percorre os elementos já guardados no banco de dados e armazena numa lista o valor do elemento lista que está no índice 3
            for x in leitura:
                armazenador.append(x[3])
        #condições para verificar se o login está de acordo com os critérios para ser criado           
                      
        if len(str(self.login.get())) <= 3:
                self.resp['text']='Digite pelo menos 4 caracteres.'
                
        if str(self.login.get()) == '':
                self.resp['text']='Preencha a caixa.'

        if len(str(self.login.get())) > 3:       
            if str(self.login.get()) in armazenador:
                    self.resp['text']='Login já existe.'
                    
            if str(self.login.get()) not in armazenador:        
                    self.resp['text']='Ok.'
        self.verSenha()

                
    def verSenha(self):
        '''
        Verifica os critérios para a criação de senha. Se a senha dadaa no cadastro
        está apta e se possui mais de 7 caracteres
        '''
        if len(str(self.senha.get())) <= 6:
                self.verificSenha['text'] = 'Digite pelo menos 7 caracteres.'
                
        if len(str(self.senha.get())) > 6:
                self.verificSenha['text'] = 'Ok.'
       
        if str(self.senha.get()) == '':
                self.verificSenha['text'] = 'Caixa vazia.'
            
        self.confirmacao()

            
    def confirmacao(self):
        '''
        verifica se a senha e login criado no cadastro, estão seguindo os critérios de verificação
        '''
        #segue as entradas de cadastro e verificam se estão Ok, depois evocam a janela para confirmação
        if self.resp['text'] == 'Ok.' and self.verificSenha['text'] == 'Ok.':
               self.cadastro()

                        
    def __init__(self):
        '''
        Janela principal do programa.
        Recolhe informações de entrada de login e senha para abrir os demais painéis
        '''
        self.janela = Tk()
        self.janela['bg']='#B8D6F0'
        self.janela.title('Login')
        self.janela.geometry('450x250+500+250')
        
        Label(self.janela,text='Login:',bg='#B8D6F0').place(x=125,y=70)
        self.login = Entry(self.janela, width = 20)
        self.login.place(x=165,y=70)
        
        Label(self.janela,text='Senha:',bg='#B8D6F0').place(x=125,y=95)
        self.senha = Entry(self.janela, show='*')
        self.senha.place(x=165,y=95)
        
        self.label_conf_login = Label(self.janela,text=' ',bg='#B8D6F0')
        self.label_conf_login.place(x=112,y=150)
        
        self.janela.resizable(False,False)
        #botões de comando
        Button(self.janela, text='Entrar', bg='orange', command=self.verifLogin).place(x=241,y=120)
        Button(self.janela, text='Cadastro', bg='orange', command=self.cad).place(x=168,y=120)
        self.janela.mainloop()

    #def agendar(self):

    def removerCad(self):
        '''
        Função recebe um ID de usuário e atualiza o banco de dados com os ID de usuário 
        que não são iguais a esse ID(não escreve o ID no banco de dados)
        '''
        #confirmação de remoção de usuário
        if messagebox.askokcancel('Remover serviços','Deseja remover esse usuário?'):
            #id de usuário recebido
            remover=int(self.tree.selection()[0])
            try:
                #faz uma leitura do banco de dados de usuários
                with open('dados_usuarios_cad.csv', mode='r', encoding='utf-8', newline='') as linhas:
                        leitura = csv.reader(linhas, delimiter=',', quotechar='"')
                        #verificador de condição
                        flag = 0
                        #armazenador de linhas
                        armazenador_dados=[]
                        for line in leitura:
                            #compara o ID do usuário que foi recebido, com o ID do banco de dados e torna o verificdor de condiçãoa, verdadeiro.
                            if int(line[6]) == remover:
                                flag=1
                                continue
                            else:
                                #adiciona dados diferentes do ID recebido
                                armazenador_dados.append(line)
                        linhas.close()
                        #a partir do verificador = True, reescreve, no banco de dados, os que foram adicionados no armazenador de dados
                        if flag == 1:
                            with open('dados_usuarios_cad.csv', mode='w', encoding='utf-8', newline='') as linhas:
                                arquivo = csv.writer(linhas)
                                for line in armazenador_dados:
                                    arquivo.writerow(line)
                                linhas.close()
                        messagebox.showinfo('Remoção','Usuário removido.')
                        self.vizualizarCadUsu()
            except:
                print('Erro1, meu jovem')

    
    def removerServ(self):
        '''
        Função recebe um ID de serviço atualiza o banco de dados com os serviços
        que não são iguais a esse ID(não escreve o ID no banco de dados)
        '''
        if messagebox.askokcancel('Remover serviços','Deseja remover esse serviço?'):
            remover=int(self.treeServ.selection()[0])
            try:
                datahora_modificacao=datetime.now()
                with open('dados_servicos.csv', mode='r', encoding='utf-8', newline='') as linhas:
                        leitura = csv.reader(linhas, delimiter=',', quotechar='"')
                        #verificador de condição
                        flag = 0
                        #guardador dos dados das linhas
                        armazenador_dados=[]
                        for line in leitura:
                            #percorre os elementos e compara de o ID do elemento é igual ao ID recebido
                            if int(line[3]) == remover:
                                if self.nivel == 2:
                                    arq = open('registro.txt','a')
                                    arq.write(f'O Subadmin {self.dadosSubAdmin[0]}, com CPF {self.dadosSubAdmin[2]}, removeu o produto {line[0]}, no valor de {line[2]}R$ Unid.  no dia {datahora_modificacao.day}/{datahora_modificacao.month}/{datahora_modificacao.year} às {datahora_modificacao.hour}:{datahora_modificacao.minute}:{datahora_modificacao.second}.\n\n')
                                    arq.close()
                                flag=1
                                continue
                            else:
                                #adiciona dados diferentes do ID recebido
                                armazenador_dados.append(line)
                        linhas.close()
                        #quando o verificador é verdadeiro, todos os dados adicionados no guardador de dados é reescrito no arquivo(banco de dados)
                        if flag ==1:
                            with open('dados_servicos.csv', mode='w', encoding='utf-8', newline='') as linhas:
                                arquivo = csv.writer(linhas)
                                for line in armazenador_dados:
                                    arquivo.writerow(line)
                                linhas.close()
                        messagebox.showinfo('Remoção','Produto removido.')
                        self.vizualizarServicos()
            except:
                print('Erro2, meu jovem')

        
    def upCad(self):
        '''
        Verifica o nível dos usuários o aumenta a um nível superior ao anterior e atualiza
        seus valores de acordo com o desejo do administrador
        '''
        #confirmação de comando
        if messagebox.askokcancel('Subir cargo','Deseja subir cargo desse usuário?'):
            iDLinha=int(self.tree.selection()[0])

            try:
                with open('dados_usuarios_cad.csv', mode='r', encoding='utf-8', newline='') as linhas:
                        leitura = csv.reader(linhas, delimiter=',', quotechar='"')
                        armazenador_dados=[]
                        aux=0
                        #percorre as linhas do banco de dados(arquivo CSV) e adiciona numa lista temp
                        for line in leitura:
                            if int(line[6]) == iDLinha:
                                #verifica se o usuário já está no cargo máximo e retorna uma mensagem se ele já estiver
                                if int(line[5]) == 2:
                                    armazenador_dados.append(line)
                                    messagebox.showinfo('Cargo','Nível máximo já alcançado.')
                                    continue
                                #verifica se o usuário está em um nível mínimo e atualiza esse valor para um nível superior   
                                if int(line[5]) == 1:
                                    aux=line
                                    aux[5]='2'
                                    armazenador_dados.append(aux)
                                    messagebox.showinfo('Cargo','Usuário atualizado para cargo de nível 2.')
                                continue
                            else:
                                armazenador_dados.append(line)
                        linhas.close() 
                        #reescreve o banco de dados com os níveis atualizados
                        with open('dados_usuarios_cad.csv', mode='w', encoding='utf-8', newline='') as linhas:
                            escrever=csv.writer(linhas)
                            for line in armazenador_dados:
                                escrever.writerow(line)
                            linhas.close()
                        self.vizualizarCadUsu()
            except:
                print('Erro3, meu jovem')


    def downCad(self):
        '''
        Verifica o nível dos usuários o rebaixa a um nível inferior e atualiza 
        seus valores de acordo com o desejo do administrador
        '''
        #confirmação de comando
        if messagebox.askokcancel('Diminuir cargo','Deseja rebaixar esse cadastro?'):
            iDLinha=int(self.tree.selection()[0])
            try:
                with open('dados_usuarios_cad.csv', mode='r', encoding='utf-8', newline='') as linhas:
                        leitura = csv.reader(linhas, delimiter=',', quotechar='"')
                        armazenador_dados=[]
                        aux=0
                        for line in leitura:
                            if int(line[6]) == iDLinha:
                                #verifica se o usuário já está no cargo minimo e retorna uma mensagem negativa se ele já estiver
                                if int(line[5]) == 1:
                                    armazenador_dados.append(line)
                                    messagebox.showinfo('Cargo','Mínimo de nível já alcançado.')

                                #verifica se o usuário está em um nível máximo e atualiza esse valor para um nível inferior
                                if int(line[5]) == 2:
                                    aux=line
                                    aux[5]='1'
                                    armazenador_dados.append(aux)
                                    messagebox.showinfo('Cargo','Cargo atualizado para usuário.')
                                continue
                            else:
                                armazenador_dados.append(line)
                        linhas.close() 
                        #reescreve o banco de dados com os níveis de usuários atualizados
                        with open('dados_usuarios_cad.csv', mode='w', encoding='utf-8', newline='') as linhas:
                            escrever=csv.writer(linhas)
                            for line in armazenador_dados:
                                #str1 = ';'.join(line)
                                escrever.writerow(line)
                            linhas.close()
                        self.vizualizarCadUsu()
            except:
                print('Erro4, meu jovem')


    def limpaCads(self):
        '''
        Faz um clear no banco de dados e limpa todos os dados dos usuários cadastrados no mesmo, exceto o de
        administrador - comando dado apenas ao adminsitrador
        '''
        #janela de confirmação para saber se deseja excluir os dados de usuários cadastrados
        if messagebox.askokcancel('Limpar cadastros','Deseja excluir todos os cadastros de usuários?'):
            try:
                #reescreve o banco de dados com todos elementos apagados
                with open('dados_usuarios_cad.csv', mode='r', encoding='utf-8', newline='') as linhas:
                        leitura = csv.reader(linhas, delimiter=',', quotechar='"')
                        armazenador_dados=[]
                        with open('dados_usuarios_cad.csv', mode='w', encoding='utf-8', newline='') as linhas:
                            escrever=csv.writer(linhas)
                            for line in armazenador_dados:
                                #str1 = ';'.join(line)
                                escrever.writerow(line)
                            linhas.close()
                        self.vizualizarCadUsu()
            except:
                print('Erro5, meu jovem')


    def limpaServ(self):
        '''
        Limpa todos os serviços encontrados no banco de dados - comando dado apenas ao adminsitrador
        '''
        #janela de confirmação para saber se deseja excluir os dados
        if messagebox.askokcancel('Limpar serviços','Deseja excluir todos os serviços?'):
            try:
                #reescreve o arquivo como none
                with open('dados_servicos.csv', mode='r', encoding='utf-8', newline='') as linhas:
                        leitura = csv.reader(linhas, delimiter=',', quotechar='"')
                        armazenador_dados=[]
                        with open('dados_servicos.csv', mode='w', encoding='utf-8', newline='') as linhas:
                            escrever=csv.writer(linhas)
                            for line in armazenador_dados:
                                #str1 = ';'.join(line)
                                escrever.writerow(line)
                            linhas.close()
                        self.vizualizarServicos()
            except:
                print('Erro6, meu jovem')
    

    def buscarProduto(self):
        '''
        Evoca uma janela para receber informação do item que o usuário quer procurar(produtos)
        '''
        #Evoca uma janela e adiciona nosvos elementos a ela ao longo das linhas
        self.janelinha = Tk()
        self.janelinha['bg']='#B8D6F0'  
        self.janelinha.resizable(False,False)
        self.janelinha.title('Buscar produtos.')
        self.janelinha.geometry('+600+300')

        Label(self.janelinha, text='Buscar pelo nome:',bg='#B8D6F0').grid(row=0, column=0, padx=4, pady=4)
        self.busca_servicos = Entry(self.janelinha)
        self.busca_servicos.grid(row=0, column=1, padx=4, pady=4)

        Button(self.janelinha, text='Procurar',command=self.produtosAchados, bg='#22467D', fg='white').grid(row=0,column=2,padx=4,pady=4)
        self.janelinha.mainloop()


    def produtosAchados(self):
        '''
        Procura o produto a partir do nome dado num input de busca e retorna 
        uma janela com uma treeview com os produtos de mesmo nome
        '''       
        self.janela.destroy()
        #Evoca uma janela e adiciona nosvos elementos a ela ao longo das linhas
        self.janela = Tk() 
        self.janela['bg']='#B8D6F0'
        self.janela.resizable(False,False) 
        self.janela.title('Serviços cadastrados')
        self.janela.geometry('+500+250')

        self.treeServ = ttk.Treeview(self.janela,selectmode='browse',column=('column1','column2','column3'), show='headings')
        
        self.treeServ.column('column1', width=150,minwidth=200,stretch=NO)
        self.treeServ.heading('#1', text='Produto')

        self.treeServ.column('column2', width=150,minwidth=200,stretch=NO)
        self.treeServ.heading('#2', text='Grupo') 

        self.treeServ.column('column3', width=100,minwidth=200,stretch=NO)
        self.treeServ.heading('#3', text='Preço R$  ') 

        self.treeServ.grid(row=0, column=0,padx=4,pady=4,rowspan=4, columnspan=3)

        #botões de comando
        Button(self.janela, text='Buscar produto', width=20, command=self.buscarProduto, bg='#22467D', fg='white').grid(row=0,column=4,sticky=S,padx=5,pady=2)
        
        if self.nivel == 2 or self.nivel == 3:
            Button(self.janela, text='Remover produto', width=20,command=self.removerServ, bg='#22467D', fg='white').grid(row=1,column=4,sticky=S,padx=2,pady=2)
            Button(self.janela, text='Atualizar produto', width=20, bg='#22467D', fg='white', command=self.janelaAtualizarProduto).grid(row=2,column=4,sticky=S,padx=5,pady=2)
            Button(self.janela, text='Voltar', width=10, command=self.atualizarInformacoes, bg='#22467D', fg='white').grid(row=5,column=0,sticky=W,padx=2,pady=2)
            if self.nivel == 3:
                Button(self.janela, text='Limpar produtos', width=20,command=self.limpaServ, bg='#22467D', fg='white').grid(row=3,column=4,sticky=S,padx=2,pady=2)
        
        else:
            if self.nivel == 1: 
                Button(self.janela, text='Adicionar ao carrinho', width=20, bg='#22467D', fg='white', command=self.adicionarCarrinho).grid(row=1,column=4,sticky=S,padx=2,pady=2)
                Button(self.janela, text='Carrinho', width=20, bg='#22467D', fg='white', command=self.carrinhoCompras).grid(row=2,column=4,sticky=S,padx=5,pady=2)
                Button(self.janela, text='Voltar', width=10, command=self.painelItens, bg='#22467D', fg='white').grid(row=5,column=0,sticky=W,padx=2,pady=2)
        
        #recebe o valor de uma entrada dada no campo de busca do programa
        buscador=self.busca_servicos.get()
        armazenadorDeLinha=[]
        #abre o arquivo CSV de usuários e procura os elmentos que são iguais ao buscador
        with open('dados_servicos.csv','r') as bancoD:
                leitura = csv.reader(bancoD)
                #percorre as linhas do arquivo e verifica se o elemento 0 de cada linha é igual ao buscador, se for, retorna treeview dos elementos iguais ao buscador
                for linha in leitura:
                    if linha[0]==buscador:                    
                        armazenadorDeLinha=linha
                        self.treeServ.insert("", END, values=armazenadorDeLinha, iid=linha[3], tag='1')
        
        messagebox.showinfo('Produtos','Todos produtos encontrados')
        self.janelinha.destroy()
        self.janela.mainloop()


    def buscarUsuario(self):
        '''
        Evoca uma janela para receber informação do item que o usuário quer procurar
        '''
        #Evoca uma janela e adiciona nosvos elementos a ela ao longo das linhas
        self.janelinha = Tk()  
        self.janelinha.resizable(False,False)
        self.janelinha['bg']='#B8D6F0'
        self.janelinha.title('Buscar Usuários.')
        self.janelinha.geometry('+600+300')

        Label(self.janelinha, text='Buscar pelo nome:',bg='#B8D6F0').grid(row=0, column=0, padx=4, pady=4)
        self.busca_usuarios = Entry(self.janelinha)
        self.busca_usuarios.grid(row=0, column=1, padx=4, pady=4)

        Button(self.janelinha, text='Procurar',command=self.usuariosAchados, bg='#22467D', fg='white').grid(row=0,column=2,padx=4,pady=4)
        self.janelinha.mainloop()


    def usuariosAchados(self):
        '''
        Procura o usuário a partir do nome de usuário dado num input e retorna
        uma janela com uma treeview com os usuários que possuem mesmo nome
        '''
        self.janela.destroy()
        #Evoca uma janela e adiciona nosvos elementos a ela ao longo das linhas
        self.janela = Tk()
        self.janela['bg']='#B8D6F0'
        self.janela.resizable(False,False)  
        self.janela.title('Cadastro Usuários')
        self.janela.geometry('+500+250')

        self.tree = ttk.Treeview(self.janela,selectmode='browse',column=('column1','column2','column3','column4','column5','column6','column7'), show='headings')
        
        self.tree.column('column1', width=100,minwidth=200,stretch=NO)
        self.tree.heading('#1', text='NOME')

        self.tree.column('column2', width=100,minwidth=200,stretch=NO)
        self.tree.heading('#2', text='ENDEREÇO') 

        self.tree.column('column3', width=80,minwidth=200,stretch=NO)
        self.tree.heading('#3', text='CPF')

        self.tree.column('column4', width=100,minwidth=200,stretch=NO)
        self.tree.heading('#4', text='LOGIN')

        self.tree.column('column5', width=100,minwidth=200,stretch=NO)
        self.tree.heading('#5', text='CÓDIGO')

        self.tree.column('column6', width=40,minwidth=200,stretch=NO)
        self.tree.heading('#6', text='NÍVEL')

        self.tree.column('column7', width=45,minwidth=200,stretch=NO)
        self.tree.heading('#7', text='ID')

        self.tree.grid(row=0, column=0,padx=4,pady=4,rowspan=5, columnspan=6)

        #botões de comando
        Button(self.janela, text='Buscar Usuário', width=20,command=self.buscarUsuario, bg='#22467D', fg='white').grid(row=0,column=7,sticky=S,padx=2,pady=2)
        if self.nivel == 3:
            Button(self.janela, text='Remover Cadastro', width=20,command=self.removerCad, bg='#22467D', fg='white').grid(row=1,column=7,sticky=S,padx=2,pady=2)
            Button(self.janela, text='Up cadastro', width=20,command=self.upCad, bg='#22467D', fg='white').grid(row=2,column=7,sticky=S,padx=5,pady=2)
            Button(self.janela, text='Down cadastro', width=20,command=self.downCad, bg='#22467D', fg='white').grid(row=3,column=7,sticky=S,padx=5,pady=2)
            Button(self.janela, text='Limpar cadastros', width=20,command=self.limpaCads, bg='#22467D', fg='white').grid(row=4,column=7,sticky=S,padx=2,pady=2)

        volta=Button(self.janela, text='Voltar', width=10, command=self.atualizarInformacoes, bg='#22467D', fg='white').grid(row=5,column=0,sticky=W,padx=2,pady=2)

        #recebe o valor de uma entrada dada no campo de busca do programa
        buscador=self.busca_usuarios.get().lower()
        armazenadorDeLinha=[]
        #abre o arquivo CSV de usuários e procura os elmentos que são iguais ao buscador
        with open('dados_usuarios_cad.csv','r') as bancoD:
                leitura = csv.reader(bancoD)
                #percorre as linhas do arquivo e verifica se o elemento 0 de cada linha é igual ao buscador, se for, retorna treeview dos elementos iguais ao buscador
                for linha in leitura:
                    if linha[0].lower()==buscador:                    
                        armazenadorDeLinha=linha
                        self.tree.insert("", END, values=armazenadorDeLinha, iid=linha[6], tag='1')
        
        messagebox.showinfo('Usuários','Todos usuários encontrados')
        self.janelinha.destroy()
        self.janela.mainloop()


    def janelaAtualizarProduto(self):
        '''
        Cria uma nova janela com as informações que vão modificar
        os parâmetros de produtos, ou seja, janela de inputs
        '''
        #Evoca uma janela e adiciona nosvos elementos a ela ao longo das linhas
        self.janelinha = Tk()
        self.janelinha['bg']='#B8D6F0'
        self.janela.resizable(False,False)
        self.janelinha.title('Atualizar serviço')
        self.janelinha.geometry('+600+300')

        Label(self.janelinha,text='Modificar nome:',bg='#B8D6F0').grid(row=0, column=0, sticky=E, padx=4, pady=4)
        self.mNome = Entry(self.janelinha)
        self.mNome.grid(row=0, column=1,columnspan=2,padx=4,pady=4)

        Label(self.janelinha,text='Modificar grupo:',bg='#B8D6F0').grid(row=1, column=0, sticky=E, padx=4, pady=4)
        self.mGrupo = Entry(self.janelinha)
        self.mGrupo.grid(row=1, column=1,columnspan=2,padx=4,pady=4)

        Label(self.janelinha,text='Modificar preço:',bg='#B8D6F0').grid(row=2, column=0, sticky=E, padx=4, pady=4)
        self.mPreco = Entry(self.janelinha)
        self.mPreco.grid(row=2, column=1,columnspan=2,padx=4,pady=4)

        #botões de comando
        Button(self.janelinha,text='Apenas o nome',command=self.atualizarNomeProduto, bg='#22467D', fg='white').grid(row=0, column=3,padx=4,pady=4)
        Button(self.janelinha,text='Apenas o preço',command=self.atualizarPrecoProduto, bg='#22467D', fg='white').grid(row=1, column=3,padx=4,pady=4)
        Button(self.janelinha,text='Modificar tudo',command=self.atualizarProduto, bg='#22467D', fg='white').grid(row=2, column=3,padx=4,pady=4)
        Button(self.janelinha,text='Cancelar',command=self.cancelarMod, bg='#22467D', fg='white').grid(row=3, column=0,sticky=W,padx=4,pady=4)
       
        self.janelinha.mainloop()


    def cancelarMod(self):
        '''
        só cancela a opção de modificação
        '''
        self.janelinha.destroy()


    def atualizarProduto(self):
        '''
        Função que reescreve no banco de dados, totalmente o produto
        selecionado e reescrito pelo administrador ou subadministrador
        '''
        messagebox.showinfo('Serviço','Serviço atualizado.')
        iDLinha=int(self.treeServ.selection()[0])
        #recolhe as informações do produto
        mNome = self.mNome.get()
        mGrupo = self.mGrupo.get()
        mPreco = self.mPreco.get()
        datahora_da_mod=datetime.now()
        arq = open('registro.txt','a')
        try:
            with open('dados_servicos.csv', mode='r', encoding='utf-8', newline='') as linhas:
                    leitura = csv.reader(linhas, delimiter=',', quotechar='"')
                    armazenador_dados=[]
                    aux=0
                    #percorre os elementos do banco de dados e recolhe o selecionado e o armazena numa variável temporária e com o nome modificado
                    for line in leitura:
                        if int(line[3]) == iDLinha:
                            #a variavel temporária recebe as novas informações do produto no formato de lista e a lista temporária adiciona essa variável                                
                            aux = [mNome,mGrupo,mPreco, str(iDLinha)]
                            armazenador_dados.append(aux)
                            if self.nivel==2:
                                arq.write(f'O usuário {self.dadosSubAdmin[0]}, com CPF {self.dadosSubAdmin[2]}, realizou uma modificação no produto {line[0]} com o ID "{line[3]}" que possuia um valor de {line[2]}R$  no dia {datahora_da_mod.day}/{datahora_da_mod.month}/{datahora_da_mod.year} às {datahora_da_mod.hour}:{datahora_da_mod.minute}:{datahora_da_mod.second}.\n\n')
                                arq.close()
                            continue
                        else:
                            armazenador_dados.append(line)
                    linhas.close() 
                    #percorre a lista temporária e reescreve o Banco de dados com as novas informações contidas nessa lista
                    with open('dados_servicos.csv', mode='w', encoding='utf-8', newline='') as linhas:
                        escrever=csv.writer(linhas)
                        for line in armazenador_dados:
                            escrever.writerow(line)
                        linhas.close()
                    self.janelinha.destroy()
                    self.vizualizarServicos()
        except:
            print('Erro7, meu jovem')
            self.janelinha.destroy()


    def atualizarNomeProduto(self):
        '''
        Função que reescreve no banco de dados, o nome atualizado do produto 
        selecionado e reescrito pelo administrador ou subadministrador
        '''
        messagebox.showinfo('Serviço','Nome atualizado.')
        iDLinha=int(self.treeServ.selection()[0])
        mNome = self.mNome.get()
        datahora_da_mod=datetime.now()
        arq = open('registro.txt','a')
        try:
            with open('dados_servicos.csv', mode='r', encoding='utf-8', newline='') as linhas:
                    leitura = csv.reader(linhas, delimiter=',', quotechar='"')
                    armazenador_dados=[]
                    aux=0
                    #percorre os elementos do banco de dados e recolhe o selecionado e o armazena numa variável temporária e com o nome modificado
                    for line in leitura:
                        if int(line[3]) == iDLinha:                                
                            aux = line

                            aux[0] = mNome
                            if self.nivel==2:
                                arq.write(f'O usuário {self.dadosSubAdmin[0]}, com CPF {self.dadosSubAdmin[2]}, realizou uma modificação no nome do produto com o ID "{line[3]}" para {line[0]} no dia {datahora_da_mod.day}/{datahora_da_mod.month}/{datahora_da_mod.year} às {datahora_da_mod.hour}:{datahora_da_mod.minute}:{datahora_da_mod.second}.\n\n')                            
                                arq.close()
                            #depois de modificadar o valor, adiciona numa lista de dados temporária
                            armazenador_dados.append(aux)
                            continue
                        else:
                            armazenador_dados.append(line)
                    linhas.close()
                    print('dsadadasd')
                    #reescreve o banco de dados, com todos os elementos presentes na lista temporária
                    with open('dados_servicos.csv', mode='w', encoding='utf-8', newline='') as linhas:
                        print('aaaaaa')
                        escrever=csv.writer(linhas)
                        for line in armazenador_dados:
                            escrever.writerow(line)
                        linhas.close()
                    self.janelinha.destroy()
                    self.vizualizarServicos()
        except:
            print('Erro8, meu jovem')
            self.janelinha.destroy()
            

    def atualizarPrecoProduto(self):
        '''
        Função que reescreve no banco de dados, o preço atualizado do produto
        selecionado e reescrito pelo administrador ou subadministrador
        '''
        messagebox.showinfo('Serviço','Preço atualizado.')
        iDLinha=int(self.treeServ.selection()[0])
        mPreco = self.mPreco.get()
        datahora_da_mod=datetime.now()
        arq = open('registro.txt','a')
        try:
            with open('dados_servicos.csv', mode='r', encoding='utf-8', newline='') as linhas:
                    leitura = csv.reader(linhas, delimiter=',', quotechar='"')
                    armazenador_dados=[]
                    aux=0
                    #percorre os elementos do banco de dados e recolhe o selecionado e o armazena numa variável temporária e com o preço modificado
                    for line in leitura:
                        if int(line[3]) == iDLinha:                                
                            aux = line
                            aux[2] = mPreco
                            if self.nivel==2:
                                arq.write(f'O usuário {self.dadosSubAdmin[0]}, com CPF {self.dadosSubAdmin[2]}, realizou uma modificação no preço do produto com o ID "{line[3]}" para o valor de {line[2]}R$  no dia {datahora_da_mod.day}/{datahora_da_mod.month}/{datahora_da_mod.year} às {datahora_da_mod.hour}:{datahora_da_mod.minute}:{datahora_da_mod.second}.\n\n')
                                arq.close()
                            #depois de modificado o valor, adiciona numa lista de dados temporária
                            armazenador_dados.append(aux)
                            continue
                        else:
                            armazenador_dados.append(line)
                    linhas.close() 
                    #reescreve o banco de dados, com todos os elementos presentes na lista temporária
                    with open('dados_servicos.csv', mode='w', encoding='utf-8', newline='') as linhas:
                        escrever=csv.writer(linhas)
                        for line in armazenador_dados:
                            escrever.writerow(line)
                        linhas.close()
                    self.janelinha.destroy()
                    self.vizualizarServicos()
        except:
            print('Erro9, meu jovem')       
            self.janelinha.destroy()


    def adicionarCarrinho(self):
        '''
        Recolhe o ID do produto selecionado pelo usuário e retona numa lista pré-definida,
        atualizando a quantidade de produtos X 
        '''
        #recolhe o valor do ID do produto
        self.idproduto=int(self.treeServ.selection()[0])
        try:
            with open('dados_servicos.csv', mode='r', encoding='utf-8', newline='') as linhas:
                    leitura = csv.reader(linhas, delimiter=',', quotechar='"')
                    #lê o arquivo CSV aberto
                    for line in leitura:
                        #verifica se o elemento "line", na posição 3, é compatível com o ID do produto selecionado
                        if int(line[3]) == self.idproduto:
                            cont=0
                            #variável para modificação da lista matriz
                            arm=[]
                            #adiciona todos os elementos do 0 ao 2 das listas contidas na lista matriz, em arm
                            for k in self.addcarrinho:
                                arm.append(k[0:3])
                            #verifica se a linha de leitura na posição 0 ao 2, já existe, se não existir, adiciona um novo elemento a lista matriz
                            if line[0:3] not in arm:
                                self.addcarrinho.append(line[0:3]+[1,line[3]]) 
                            
                            else:
                                #vai percorrer os elementos da lista matriz e verificar se a linha de leitura é igual a algum dos elemento na lista matriz,
                                #se for, ele adiciona uma nova quantidade do produto selecionado
                                for elem in self.addcarrinho:
                                    if line[0:3] == elem[0:3]:
                                        self.addcarrinho[cont][3]+=1
                                        continue
                                    cont+=1
                                cont=0
                                
                    messagebox.showinfo('Carrinho','Produto adicionado ao carrinho.')
        except:
            print('Erro10, meu jovem')

    def carrinhoCompras(self):
        '''
        Cria uma janela de informações e adiciona uma lista de valores, recolhida num banco de dados,
        a uma treeview para ser mostrada ao usuário
        '''
        self.janela.destroy()
        #Evoca uma janela e adiciona nosvos elementos a ela ao longo das linhas
        self.janela = Tk() 
        self.janela['bg']='#B8D6F0' 
        self.janela.resizable(False,False)
        self.janela.title('Produtos no carrinho')
        self.janela.geometry('+500+250')

        #tabela de informações
        self.treeServ = ttk.Treeview(self.janela,selectmode='browse',column=('column1','column2','column3','column4'), show='headings')
            
        self.treeServ.column('column1', width=150,minwidth=200,stretch=NO)
        self.treeServ.heading('#1', text='Produto')

        self.treeServ.column('column2', width=150,minwidth=200,stretch=NO)
        self.treeServ.heading('#2', text='Grupo') 

        self.treeServ.column('column3', width=100,minwidth=200,stretch=NO)
        self.treeServ.heading('#3', text='Preço R$  ') 

        self.treeServ.column('column4', width=75,minwidth=200,stretch=NO)
        self.treeServ.heading('#4', text='Qnt.  ') 

        self.treeServ.grid(row=0, column=0,padx=4,pady=4,rowspan=4, columnspan=3)
        #botões de comando
        Button(self.janela, text='Finalizar pedido(s)', width=20, bg='#22467D', fg='white', command=self.finalizarPedido).grid(row=0,column=4,sticky=S,padx=5,pady=2)
        Button(self.janela, text='Finalizar todos pedidos', width=20, bg='#22467D', fg='white', command=self.finalizarTodosPedidos).grid(row=1,column=4,sticky=S,padx=5,pady=2)
        Button(self.janela, text='Remover item', width=20, bg='#22467D', fg='white', command=self.cancelarPedido).grid(row=2,column=4,sticky=S,padx=5,pady=2)
        Button(self.janela, text='Cancelar todos os itens', width=20, bg='#22467D', fg='white', command=self.cancelarTodosPedidos).grid(row=3,column=4,sticky=S,padx=5,pady=2)  

        Button(self.janela, text='Voltar', width=10, command=self.painelItens, bg='#22467D', fg='white').grid(row=5,column=0,sticky=W,padx=2,pady=2)
        #recolhe informação de uma lista definida e a adioca os valores de cada elemento, numa tabela(treeview)
        for elem in self.addcarrinho:
                self.treeServ.insert("", END, values=elem, iid=elem[4], tag='1')
        
        self.janela.mainloop()

   
    def finalizarPedido(self):
        '''
        Verifica os itens no carrinho de compra do usuário e finaliza a compra se o mesmo aceitar e
        armazena os dados do comprador e do item comprando, num banco de dados.
        '''
        idproduto=int(self.treeServ.selection()[0])
        #caixa para aceitar a finalização de compra
        if messagebox.askokcancel('Carrinho','Clique em ok para finalizar a compra.'):
            try:
                #variável para guardar informações de usuário e itens comprados                
                armazenador_dados=[]
                arq = open('registro.txt','a')
                datahora_da_compra=datetime.now()
                with open('dados_servicos.csv', mode='r', encoding='utf-8', newline='') as linhas:
                        leitura = csv.reader(linhas, delimiter=',', quotechar='"')
                        for line in leitura:
                            #verifica se um elem da linha do CSV é igual ao ID selecionado do produto                            
                            if int(line[3]) == idproduto:
                                for elem in self.addcarrinho:
                                    #virifica se há alguma produto no carrinho com o id selecionado
                                    if int(elem[4]) == idproduto:
                                        #escreve as informações de compra e do usuário, no banco de dados
                                        with open('dados_de_compras_usu.csv', mode='a', encoding='utf-8', newline='') as compras:
                                            escrever=csv.writer(compras)
                                            valor_produto_arredondado=2
                                            armazenador_dados.append([self.dadosUsu[0],self.dadosUsu[2]]+elem[0:4]+[f'{datahora_da_compra.day}/{datahora_da_compra.month}/{datahora_da_compra.year}',f'{datahora_da_compra.hour}:{datahora_da_compra.minute}:{datahora_da_compra.second}'])                                            
                                            arq.write(f'O usuário {self.dadosUsu[0]}, com CPF {self.dadosUsu[2]}, realizou uma compra do produto {elem[0]} com uma Qntd.x{elem[3]}, no valor de {float(elem[2])*int(elem[3]):.2f}R$  no dia {datahora_da_compra.day}/{datahora_da_compra.month}/{datahora_da_compra.year} às {datahora_da_compra.hour}:{datahora_da_compra.minute}:{datahora_da_compra.second}.\n\n')
                                            arq.close()
                                            for line in armazenador_dados:
                                                escrever.writerow(line)
                                                compras.close()
                                        messagebox.showinfo('Carrinho','Pedido finalizado com sucesso.')
                                        self.addcarrinho.remove(elem)
                                        self.carrinhoCompras()

            except:
                print('Erro11, meu jovem')
    

    def finalizarTodosPedidos(self):
        '''
        Armazena as informações do pedido realizado por um usuário e coloca num banco de dados 
        junto com as informações do usuário, data e hora da compra
        '''
        #janela de confirmação para saber se deseja finalizaar oo pedidos
        if messagebox.askokcancel('Carrinho','Deseja finalizar o pedido de todos os itens?.'):
            try: 
                arq = open('registro.txt','a')
                #verifica o horário e data
                datahora_da_compra=datetime.now()
                #escreve o banco as novas informações recebidas de compra
                with open('dados_de_compras_usu.csv', mode='a', encoding='utf-8', newline='') as compras:
                    escrever=csv.writer(compras, delimiter=',', quotechar='"')
                    #variável que irá guardar as informações ampliadas
                    armazenador_dados=[]
                    #percorre os elementos já adicionados no carrinho
                    for elem in self.addcarrinho: 
                        #amplia as informações da compra do usuário, adicionando data e informações do mesmo (CPF, nome)
                        armazenador_dados.append([self.dadosUsu[0],self.dadosUsu[2]]+elem[0:4]+[f'{datahora_da_compra.day}/{datahora_da_compra.month}/{datahora_da_compra.year}', f'{datahora_da_compra.hour}:{datahora_da_compra.minute}:{datahora_da_compra.second}'])
                        arq.write(f'O usuário {self.dadosUsu[0]}, com CPF {self.dadosUsu[2]}, realizou uma compra do produto {elem[0]} em uma Qntd.x{elem[3]} no valor de {float(elem[2])*int(elem[3]):.2f}R$  no dia {datahora_da_compra.day}/{datahora_da_compra.month}/{datahora_da_compra.year} às {datahora_da_compra.hour}:{datahora_da_compra.minute}:{datahora_da_compra.second}.\n\n')
                    #escreve as informações ampliadas de compra e que foram armazenadas numa lista de listas
                    for line in armazenador_dados:
                        escrever.writerow(line)    
                    compras.close()
                    arq.close()
                    messagebox.showinfo('Carrinho','Pedidos finalizados com sucesso.')
                    self.addcarrinho.clear()
                    self.carrinhoCompras()
                    self.vizualizarCadUsu()
                
                
            except:
                print('Erro12, meu jovem')

        
    def cancelarPedido(self):
        '''
        Função para remover, dado um ID, o ID do produto que foi adicionado a treeview do carrinho
        e retornar a janela com informações atualizadas
        '''
        idproduto=int(self.treeServ.selection()[0])
        arq = open('registro.txt','a')
        #janela de confirmação para saber se deseja remover um item do carrinho
        if messagebox.askokcancel('Carrinho','Deseja remover o item do carrinho?.'):
            try:
                with open('dados_servicos.csv', mode='r', encoding='utf-8', newline='') as linhas:
                        leitura = csv.reader(linhas, delimiter=',', quotechar='"')
                        for line in leitura:
                            #verifica se se um elem da linha do CSV é igual ao ID selecionado do produto
                            if int(line[3]) == idproduto:
                                for elem in self.addcarrinho:
                                    #verifica se o elem de uma lista de produtos adicionados no carrinho, é igual ao id do produto, se for, o remove
                                    if int(elem[4]) == idproduto:
                                        self.addcarrinho.remove(elem)

                        messagebox.showinfo('Carrinho','Item removido do carrinho.')
                        self.carrinhoCompras()
            except:
                print('Erro13, meu jovem')

    def cancelarTodosPedidos(self):
        '''
        Faz um clear no banco de dados e limpa todos os dados de itens adicionados ao carrinho pelo usuário
        '''
        #janela de confirmação para saber se deseja excluir os dados dos items no carrinho
        if messagebox.askokcancel('Carrinho','Deseja cancelar todos os itens?.'):
            try:
                #reescreve o banco de dados com todos elementos apagados
                with open('dados_de_compras_usu.csv', mode='w', encoding='utf-8', newline='') as linhas:
                    leitura = csv.writer(linhas, delimiter=',', quotechar='"')
                    armazenador_dados=[]
                    escrever=csv.writer(linhas)
                    self.addcarrinho=[]
                    for elem in self.addcarrinho:
                        escrever.writerow(elem)
                        linhas.close()
                    messagebox.showinfo('Carrinho','Pedidos cancelados com sucesso.')
                    self.carrinhoCompras()
            except:
                print('Erro14, meu jovem')

    def informacoesDeConta(self):
        '''
        Função que evoca uma janela para a verificação dos dados cadastrais que o usuário possui
        '''
        self.janela.destroy()
        self.janela = Tk()
        self.janela['bg']='#B8D6F0'
        self.janela.resizable(False,False)
        self.janela.title('Informações usuário')
        self.janela.geometry('+500+250')

        Label(self.janela, text='Nome: ',bg='#B8D6F0').grid(row=1, column=1, sticky=E, padx=4, pady=4)
        Label(self.janela, text='Endereço: ',bg='#B8D6F0').grid(row=2, column=1, columnspan=2, sticky=E, padx=4, pady=4)
        Label(self.janela, text='CPF: ',bg='#B8D6F0').grid(row=3, column=1,columnspan=2, sticky=E, padx=4, pady=4)
        Label(self.janela, text='Login: ',bg='#B8D6F0').grid(row=4, column=1,columnspan=2, sticky=E, padx=4, pady=4)
        Label(self.janela, text='Senha: ',bg='#B8D6F0').grid(row=5, column=1,columnspan=2, sticky=E, padx=4, pady=4)
        Label(self.janela, text=f'{self.dadosUsu[0]}',bg='#B8D6F0').grid(row=1, column=3, sticky=W,columnspan=2, padx=4, pady=4)
        self.labelEndereco=Label(self.janela, text=f'{self.dadosUsu[1]}',bg='#B8D6F0')
        self.labelEndereco.grid(row=2, column=3,columnspan=2, sticky=W, padx=4, pady=4)
        Label(self.janela, text=f'{self.dadosUsu[2]}',bg='#B8D6F0').grid(row=3, column=3, columnspan=2, sticky=W, padx=4, pady=4)
        Label(self.janela, text=f'{self.dadosUsu[3]}',bg='#B8D6F0').grid(row=4, column=3, columnspan=2, sticky=W, padx=4, pady=4)
        Label(self.janela, text='*******',bg='#B8D6F0').grid(row=5, column=3, columnspan=2, sticky=W, padx=4, pady=4)
        
        #botões de comando
        Button(self.janela, text='Editar endereço', command=self.janEditadorEnd, bg='#22467D', fg='white').grid(row=2,column=5, sticky=W,padx=4,pady=4)
        Button(self.janela, text='Editar Senha', bg='#22467D', fg='white', command=self.janEditadorSenha).grid(row=5,column=5, sticky=W,padx=4,pady=4)
        Button(self.janela, text='Voltar', command=self.atualizarInformacoes, bg='#22467D', fg='white').grid(row=6,column=1, sticky=E,padx=4,pady=4)

        self.janela.mainloop()


    def janEditadorEnd(self):
        '''
        Evoca uma janela de modificação da informação escolhida pelo usuário, no caso, Endereço
        '''
        self.janelinha = Tk()
        self.janelinha['bg']='#B8D6F0'
        self.janelinha.resizable(False,False)
        self.janelinha.title('Editar usuário')
        self.janelinha.geometry('+500+250')

        Label(self.janelinha, text='Novo endereço: ',bg='#B8D6F0').grid(row=1, column=1, sticky=E, padx=4, pady=4)
        self.novoEnd = Entry(self.janelinha)
        self.novoEnd.grid(row=1, column=2, padx=4, pady=4)

        #botão de comando
        Button(self.janelinha, text='Confirmar',command=self.edicaoEnd,bg='#22467D').grid(row=1, column=3, sticky=E, padx=4, pady=4)
        
        self.janelinha.mainloop()


    def edicaoEnd(self):
        '''
        Função que capta o dado fornecido na modificação do endereço e reescreve no banco de dados essa informação atualizada do usuário
        '''
        #condição para o usuário prosseguir ou não com a modificação
        if messagebox.askokcancel('Edição End.','Clique em ok para atualizar seus dados.'):
            try:
                #faz leitura do arquivo csv e armazena seus dados numa variável do tipo lista
                with open('dados_usuarios_cad.csv', mode='r', encoding='utf-8', newline='') as linhas:
                        leitura = csv.reader(linhas, delimiter=',', quotechar='"')
                        armazenador=[]
                        aux=0
                        for line in leitura:
                            #verifica o id da linha do arquivo lido, é igual ao ID do usuário                            
                            if line[6] == self.dadosUsu[6]:
                                aux=line
                                #a variável serve como guardador de dados temporários e reescreve o elemento captado com a nova informação
                                aux[1]=self.novoEnd.get()
                                #atualiza as informações do usuário
                                self.dadosUsu=aux
                                armazenador.append(aux)                              
                            else:
                                armazenador.append(line)
                        linhas.close()
                #abre o banco de dados no modo de escrita e atualiza a informação do usuário para a nova
                with open('dados_usuarios_cad.csv', mode='w', encoding='utf-8', newline='') as linhas:
                    escrever=csv.writer(linhas)
                    for line in armazenador:
                        escrever.writerow(line)
                    linhas.close()
                            
                    messagebox.showinfo('Edição End.','Endereço editado!.')
                    self.informacoesDeConta()
                    self.janelinha.destroy()
            except:
                print('Erro15, meu jovem')
        

    def janEditadorSenha(self):
        '''
        Evoca uma janela de modificação da informação escolhida pelo usuário, no caso, Senha
        '''
        self.janelinha = Tk()
        self.janelinha['bg']='#B8D6F0'
        self.janelinha.resizable(False,False)
        self.janelinha.title('Editar usuário')
        self.janelinha.geometry('+500+250')

        Label(self.janelinha, text='Nova senha: ',bg='#B8D6F0').grid(row=1, column=1, sticky=E, padx=4, pady=4)
        self.lbnovaSenha = Label(self.janelinha, text=' ',bg='#B8D6F0')
        self.lbnovaSenha.grid(row=2, column=1, columnspan=2, sticky=W, padx=4, pady=4)

        self.novaSenha = Entry(self.janelinha)
        self.novaSenha.grid(row=1, column=2, padx=4, pady=4)
        #botão de comando
        Button(self.janelinha, text='Confirmar',command=self.verificarNovaSenha,bg='#22467D', ).grid(row=1, column=3, sticky=E, padx=4, pady=4)
        self.janelinha.mainloop()


    def verificarNovaSenha(self):
        '''
        Função para verificar se a modificação de senha, atende aos padrões estabelecidos no cadastro, quantidade de caractes e etc.
        '''
        if len(str(self.novaSenha.get())) <= 6:
            self.lbnovaSenha['text'] = 'Digite pelo menos 7 caracteres.'
                
        if len(str(self.novaSenha.get())) > 6:
                self.lbnovaSenha['text'] = 'Ok.'
                self.edicaoSenha()
                self.janelinha.destroy() 


    def edicaoSenha(self):
        '''
        Função que capta o dado fornecido na modificação de senha e reescreve no banco de dados essa informação atualizada do usuário
        '''
        #condição para o usuário prosseguir ou não com a modificação
        if messagebox.askokcancel('Edição End.','Clique em ok para atualizar seus dados.'):
            try:
                with open('dados_usuarios_cad.csv', mode='r', encoding='utf-8', newline='') as linhas:
                        leitura = csv.reader(linhas, delimiter=',', quotechar='"')
                        armazenador=[]
                        aux=0
                        for line in leitura:
                            #verifica o id da linha do arquivo lido, é igual ao ID do usuário                            
                            if line[6] == self.dadosUsu[6]:
                                aux=line
                                #a variável serve como guardador de dados temporários e reescreve o elemento captado com a nova informação
                                aux[4]= ','.join([str(ord(x)**71 % 1073) for x in str(self.novaSenha.get())])
                                armazenador.append(aux)
                                #atualiza informação de usuário
                                self.dadosUsu=aux
                            else:
                                armazenador.append(line)
                        linhas.close()
                #abre o banco de dados no modo de escrita e atualiza a informação do usuário para a nova
                with open('dados_usuarios_cad.csv', mode='w', encoding='utf-8', newline='') as linhas:
                    escrever=csv.writer(linhas)
                    for line in armazenador:
                        escrever.writerow(line)
                    linhas.close()
                    self.informacoesDeConta()
                            
                messagebox.showinfo('Edição End.','Senha atualizada!.')
            except:
                print('Erro16, meu jovem')

usu.close()
serv.close
compras_usu.close()
print(dicio_user)
Programa()

