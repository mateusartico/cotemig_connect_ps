# Cotemig Connect

Sistema de gerenciamento de monitorias acadêmicas desenvolvido para facilitar a conexão entre alunos e monitores.

## Sobre o Projeto

O Cotemig Connect é uma plataforma web que permite aos alunos encontrar e agendar monitorias, enquanto os monitores podem criar e gerenciar suas sessões de ensino. O sistema inclui funcionalidades como busca avançada, sistema de avaliações e suporte integrado.

## Requisitos Funcionais Implementados

**RF01** - Cadastro de usuários com informações básicas (nome, email, tipo)

**RF02** - Sistema de login seguro com validação de credenciais

**RF03** - Redefinição de senha através de token de recuperação

**RF04** - Verificação de conta por código de 6 dígitos

**RF05** - Detecção automática de tipo de usuário por padrão de email

**RF06** - Validação de email institucional (@cotemig.com.br e @aluno.cotemig.com.br)

**RF07** - Criação de monitorias pelos monitores

**RF08** - Agendamento de sessões com data, hora e local

**RF09** - Sistema de reserva de vagas pelos alunos

**RF10** - Cancelamento de reservas

**RF11** - Controle de vagas disponíveis em tempo real

**RF12** - Geração de código de presença pelo monitor

**RF13** - Registro de presença dos alunos via código

**RF14** - Busca avançada por palavras-chave

**RF15** - Filtros de busca por categoria e avaliação

**RF16** - Sistema de avaliações de 1-5 estrelas

**RF17** - Comentários nas avaliações

**RF18** - Histórico de buscas realizadas pelo usuário

**RF19** - Comparador lado a lado de múltiplas monitorias

**RF20** - Sistema de tickets de suporte

**RF21** - Dashboard personalizado por tipo de usuário

**RF22** - Interface responsiva para dispositivos móveis

**RF23** - Sistema de notificações em tempo real

**RF24** - Controle de sessões seguro

**RF25** - Logs de auditoria das ações dos usuários

## Observações importantes

Os requisitos 3 e 4 ainda não estão completos. A lógica deles funciona perfeitamente, mas a ideia é enviar os códigos de verificação por email, usando uma api e js

## Funcionalidades por Usuário

### Alunos
- Buscar e filtrar monitorias
- Reservar e cancelar vagas
- Registrar presença via código
- Avaliar monitorias participadas
- Visualizar histórico de buscas
- Abrir tickets de suporte

### Monitores
- Criar e gerenciar monitorias
- Controlar vagas e participantes
- Gerar códigos de presença
- Iniciar e finalizar sessões
- Visualizar avaliações recebidas

### Administradores
- Gerenciar usuários do sistema
- Responder tickets de suporte
- Visualizar logs de auditoria
- Configurações gerais

## Estrutura do Projeto

```
cotemig_connect_ps/
├── app/
│   ├── controllers/        # Lógica de controle
│   ├── models/            # Modelos de dados
│   ├── repositories/      # Acesso aos dados
│   ├── services/          # Lógica de negócio
│   ├── core/              # Funcionalidades centrais
│   ├── templates/         # Interface do usuário
│   └── static/           # Arquivos estáticos
├── config/               # Configurações
└── instance/            # Banco de dados
```

## Arquitetura

O sistema utiliza arquitetura MVC (Model-View-Controller) com padrões de projeto para organização e manutenibilidade:

- **Model**: Entidades e regras de negócio (`app/models/`)
- **View**: Templates e interface (`app/templates/`)
- **Controller**: Lógica de controle (`app/controllers/`)
- **Repository**: Abstração de acesso a dados
- **Factory**: Criação padronizada de objetos
- **Observer**: Sistema de notificações
- **Strategy**: Algoritmos intercambiáveis
- **Singleton**: Conexão única com banco

## Tecnologias

- **Backend**: Flask + SQLAlchemy
- **Frontend**: HTML5 + CSS3 + JavaScript
- **Banco de Dados**: SQLite
- **Segurança**: bcrypt para senhas, controle de sessões

## Como Executar

1. Instalar dependências:
```bash
pip install -r requirements.txt
```

2. Popular o banco de dados:
```bash
python seed_data.py
```

3. Executar a aplicação:
```bash
python run.py
```

4. Acessar: http://localhost:5001

## Testes

Para testar os padrões implementados:
```bash
python test_padroes.py
```

## Usuários de Teste

- **Admin**: admin@cotemig.com.br / admin123
- **Monitor 1**: monitor-mateusartico@cotemig.com.br / monitor123
- **Monitor 2**: monitor-anaelisa@cotemig.com.br / monitor123
- **Aluno 1**: 22301461@aluno.cotemig.com.br / aluno123
- **Aluno 2**: 22302832@aluno.cotemig.com.br / aluno123

## Equipe

- Arthur Vinicius – 22301852
- Daniel Bitencourt – 22301461
- Eduarda de Oliveira Neves – 22401300
- Giovanni Antônio – 22302832
- Mateus Artico – 22301542
- Pablo Alex – 22302514