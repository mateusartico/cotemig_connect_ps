from app import create_app, db
from app.models.entities import Usuario, Disciplina

def seed_database():
    app = create_app()
    
    with app.app_context():
        # Dropar e recriar todas as tabelas
        db.drop_all()
        db.create_all()
        
        # Criar disciplinas com categorias
        disciplinas = [
            {'nome': 'Programação I', 'codigo': 'PROG1', 'categoria': 'Programação'},
            {'nome': 'Programação II', 'codigo': 'PROG2', 'categoria': 'Programação'},
            {'nome': 'Banco de Dados', 'codigo': 'BD', 'categoria': 'Banco de Dados'},
            {'nome': 'Estrutura de Dados', 'codigo': 'ED', 'categoria': 'Programação'},
            {'nome': 'Redes de Computadores', 'codigo': 'REDES', 'categoria': 'Redes'},
            {'nome': 'Engenharia de Software', 'codigo': 'ES', 'categoria': 'Engenharia'},
        ]
        
        for disc_data in disciplinas:
            disciplina = Disciplina(**disc_data)
            db.session.add(disciplina)
        
        # Criar usuário admin
        admin = Usuario(
            nome='Administrador',
            email='admin@cotemig.com.br',
            tipo='admin',
            ativo=True,
            verificado=True
        )
        admin.set_password('admin123')
        db.session.add(admin)
        
        # Criar monitor exemplo
        monitor = Usuario(
            nome='João Silva',
            email='joao.silva@cotemig.com.br',
            tipo='monitor',
            ativo=True,
            verificado=True
        )
        monitor.set_password('monitor123')
        db.session.add(monitor)
        
        # Criar aluno exemplo
        aluno = Usuario(
            nome='Maria Santos',
            email='maria.santos@aluno.cotemig.com.br',
            tipo='aluno',
            ativo=True,
            verificado=True
        )
        aluno.set_password('aluno123')
        db.session.add(aluno)
        
        db.session.commit()
        print("Banco de dados populado com sucesso!")
        print("\nUsuarios criados:")
        print("Admin: admin@cotemig.com.br / admin123")
        print("Monitor: joao.silva@cotemig.com.br / monitor123")
        print("Aluno: maria.santos@aluno.cotemig.com.br / aluno123")
        print("\nNovas funcionalidades:")
        print("- Busca avancada com filtros")
        print("- Sistema de avaliacoes")
        print("- Historico de buscas")
        print("- Comparador de monitorias")
        print("- Central de suporte")
        print("- Recuperacao de senha")

if __name__ == '__main__':
    seed_database()