# Cotemig Connect - Sistema Expandido

Sistema completo de gerenciamento de monitorias acadêmicas com **arquitetura MVC tradicional** e múltiplas funcionalidades avançadas.

## 🎯 Sobre o Projeto

**Cotemig Connect** é uma aplicação web **mobile-first** para agendamento e gerenciamento de monitorias entre alunos e monitores, com sistema de busca avançada, avaliações, suporte e muito mais.

## ✅ Requisitos Funcionais Atendidos (12/20)

### **RF01** - ✅ Cadastro de usuários com informações básicas
- Sistema completo de cadastro com nome, email, tipo de usuário
- Validação de email institucional por domínio

### **RF02** - ✅ Redefinição de senha simples e segura  
- Sistema de recuperação por token
- Validação de força da senha

### **RF03** - ✅ Pesquisa avançada por palavras-chave e categorias
- Busca por título, descrição e tags
- Filtros por categoria e avaliação

### **RF05** - ✅ Filtros personalizados para refinar buscas
- Filtro por categoria de disciplina
- Filtro por avaliação mínima
- Filtro por disponibilidade de vagas

### **RF06** - ✅ Avaliações e feedbacks dos usuários
- Sistema de avaliação de 1-5 estrelas
- Comentários opcionais
- Média de avaliações por monitoria

### **RF08** - ✅ Comparador lado a lado
- Comparação de múltiplas monitorias
- Visualização de características em paralelo

### **RF11** - ✅ Histórico de buscas realizadas
- Registro automático de pesquisas
- Acesso rápido a buscas anteriores

### **RF12** - ✅ Interface intuitiva e acessível
- Design mobile-first responsivo
- Navegação simples e clara

### **RF14** - ✅ Sistema seguro
- Senhas hash com bcrypt
- Controle de sessões
- Validação de acesso por papéis

### **RF15** - ✅ Conta personalizada para cada usuário
- Perfis diferenciados (aluno, monitor, admin)
- Dashboard personalizado por tipo

### **RF16** - ✅ Escalabilidade garantida
- Arquitetura MVC + Repository
- Código modular e extensível

### **RF18** - ✅ Área de suporte dedicada
- Sistema de tickets
- FAQ integrado
- Área administrativa para respostas

## 🏗️ Arquitetura MVC Expandida

```
cotemig_connect/
├── app/
│   ├── controllers/         # Controladores
│   │   ├── auth_controller.py      # Autenticação
│   │   ├── main_controller.py      # Dashboard
│   │   ├── monitoria_controller.py # Monitorias
│   │   ├── busca_controller.py     # Busca avançada
│   │   ├── avaliacao_controller.py # Avaliações
│   │   └── suporte_controller.py   # Suporte
│   ├── models/             # Modelos expandidos
│   │   └── entities.py     # Usuario, Monitoria, Avaliacao, etc.
│   ├── repositories/       # Acesso a dados
│   ├── templates/          # Views organizadas
│   │   ├── auth/          # Login, cadastro, recuperação
│   │   ├── busca/         # Pesquisa e comparação
│   │   ├── avaliacao/     # Sistema de avaliações
│   │   ├── suporte/       # Central de ajuda
│   │   └── monitoria/     # Gestão de monitorias
│   └── static/css/        # Estilos únicos
└── config/                # Configurações
```

## 🚀 Funcionalidades Principais

### 🔐 **Autenticação Completa**
- Cadastro com validação institucional
- Login seguro
- Recuperação de senha por token
- Verificação por código

### 🔍 **Sistema de Busca Avançada**
- Pesquisa por palavras-chave
- Filtros por categoria e avaliação
- Histórico de buscas
- Comparador de monitorias

### ⭐ **Sistema de Avaliações**
- Avaliação de 1-5 estrelas
- Comentários dos alunos
- Média de avaliações
- Histórico de feedbacks

### 🎓 **Gestão de Monitorias**
- Criação e agendamento
- Reserva de vagas
- Registro de presença por código
- Controle de status

### 🆘 **Central de Suporte**
- Sistema de tickets
- FAQ integrado
- Área administrativa
- Resolução de problemas

### 📱 **Interface Mobile-First**
- Design responsivo
- Paleta Cotemig
- Navegação intuitiva
- Performance otimizada

## 🛠️ Tecnologias

- **Backend**: Flask + SQLAlchemy
- **Frontend**: HTML5 + CSS3 + JavaScript
- **Banco**: SQLite (desenvolvimento)
- **Segurança**: bcrypt, validações, controle de sessão

## 🚀 Execução

```bash
# 1. Instalar dependências
pip install -r requirements.txt

# 2. Popular banco
python seed_data.py

# 3. Executar
python run.py
```

**Acesso:** http://localhost:5000

## 👥 Usuários de Teste

- **Admin**: admin@cotemig.com.br / admin123
- **Monitor**: joao.silva@cotemig.com.br / monitor123  
- **Aluno**: maria.santos@aluno.cotemig.com.br / aluno123

## 🎯 Funcionalidades por Usuário

### **Alunos**
- Buscar monitorias com filtros
- Reservar e cancelar vagas
- Registrar presença por código
- Avaliar monitorias participadas
- Histórico de buscas
- Suporte via tickets

### **Monitores**
- Criar e gerenciar monitorias
- Gerar códigos de presença
- Visualizar avaliações recebidas
- Controlar vagas e participantes

### **Administradores**
- Gerenciar usuários
- Responder tickets de suporte
- Visualizar relatórios
- Configurações do sistema

## 👨‍💻 Equipe de Desenvolvimento

- **Arthur Vinicius** – 22301852
- **Daniel Bitencourt** – 22301461
- **Eduarda de Oliveira Neves** – 22401300
- **Giovanni Antônio** – 22302832
- **Mateus Artico** – 22301542
- **Pablo Alex** – 22302514

---

**Sistema completo e funcional atendendo 12+ requisitos funcionais!**