#!/usr/bin/env python3
"""
Testes para demonstrar o funcionamento dos padrões de projeto
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.core.database_singleton import DatabaseSingleton, database
from app.core.factory import EntityFactoryProvider
from app.core.observer import MonitoriaSubject, NotificationObserver
from app.core.strategy import SearchContext, TitleSearchStrategy, FullTextSearchStrategy
from app.repositories.usuario_repository import UsuarioRepository

def test_singleton():
    """Testa o padrão Singleton"""
    print("🔒 Testando Padrão Singleton...")
    
    # Criar múltiplas instâncias
    db1 = DatabaseSingleton()
    db2 = DatabaseSingleton()
    db3 = database
    
    # Verificar se são a mesma instância
    assert db1 is db2, "Singleton falhou: instâncias diferentes"
    assert db1 is db3, "Singleton falhou: instância global diferente"
    assert db1.db is db2.db, "Singleton falhou: objetos SQLAlchemy diferentes"
    
    print("✅ Singleton funcionando corretamente - uma única instância")

def test_factory():
    """Testa o padrão Factory Method"""
    print("\n🏭 Testando Padrão Factory Method...")
    
    # Criar usuário via factory
    usuario_data = {
        'nome': 'Teste Factory',
        'email': 'teste@cotemig.com.br',
        'tipo': 'monitor',
        'senha': 'senha123'
    }
    
    usuario = EntityFactoryProvider.create_entity('usuario', **usuario_data)
    
    assert usuario.nome == 'Teste Factory', "Factory falhou: nome incorreto"
    assert usuario.email == 'teste@cotemig.com.br', "Factory falhou: email incorreto"
    assert usuario.tipo == 'monitor', "Factory falhou: tipo incorreto"
    assert usuario.check_password('senha123'), "Factory falhou: senha não foi definida"
    
    print("✅ Factory Method funcionando corretamente - objeto criado com sucesso")

def test_observer():
    """Testa o padrão Observer"""
    print("\n👁️ Testando Padrão Observer...")
    
    # Criar subject e observer
    subject = MonitoriaSubject()
    observer = NotificationObserver("Teste")
    
    # Anexar observer
    subject.attach(observer)
    
    # Disparar evento
    subject.criar_monitoria({
        'id': 1,
        'titulo': 'Monitoria Teste',
        'monitor_id': 1
    })
    
    # Verificar se observer foi notificado
    assert len(observer.notifications) == 1, "Observer falhou: notificação não recebida"
    assert observer.notifications[0]['type'] == 'monitoria_criada', "Observer falhou: tipo incorreto"
    
    print("✅ Observer funcionando corretamente - notificação recebida")

def test_strategy():
    """Testa o padrão Strategy"""
    print("\n🎯 Testando Padrão Strategy...")
    
    # Criar objetos de teste
    class MockMonitoria:
        def __init__(self, titulo, descricao="", tags=""):
            self.titulo = titulo
            self.descricao = descricao
            self.tags = tags
    
    monitorias = [
        MockMonitoria("Python Básico", "Curso de Python", "python,programacao"),
        MockMonitoria("Java Avançado", "Curso avançado de Java", "java,oop"),
        MockMonitoria("Banco de Dados", "SQL e NoSQL", "sql,database")
    ]
    
    # Testar estratégia de busca por título
    context = SearchContext(TitleSearchStrategy())
    results = context.execute_search("Python", monitorias)
    
    assert len(results) == 1, "Strategy falhou: resultado incorreto para busca por título"
    assert results[0].titulo == "Python Básico", "Strategy falhou: monitoria incorreta"
    
    # Trocar estratégia
    context.set_strategy(FullTextSearchStrategy())
    results = context.execute_search("SQL", monitorias)
    
    assert len(results) == 1, "Strategy falhou: resultado incorreto para busca completa"
    assert results[0].titulo == "Banco de Dados", "Strategy falhou: monitoria incorreta"
    
    print("✅ Strategy funcionando corretamente - algoritmos intercambiáveis")

def test_repository():
    """Testa o padrão Repository"""
    print("\n📚 Testando Padrão Repository...")
    
    app = create_app()
    with app.app_context():
        repo = UsuarioRepository()
        
        # Testar métodos do repository
        assert hasattr(repo, 'create'), "Repository falhou: método create não existe"
        assert hasattr(repo, 'get_by_id'), "Repository falhou: método get_by_id não existe"
        assert hasattr(repo, 'get_all'), "Repository falhou: método get_all não existe"
        assert hasattr(repo, 'find_by'), "Repository falhou: método find_by não existe"
        assert hasattr(repo, 'get_by_email'), "Repository falhou: método específico não existe"
        
        print("✅ Repository funcionando corretamente - interface implementada")

def test_mvc_separation():
    """Testa a separação MVC"""
    print("\n🏗️ Testando Separação MVC...")
    
    # Verificar estrutura de diretórios
    import os
    
    base_path = os.path.dirname(os.path.abspath(__file__))
    app_path = os.path.join(base_path, 'app')
    
    # Model
    models_path = os.path.join(app_path, 'models')
    assert os.path.exists(models_path), "MVC falhou: diretório models não existe"
    assert os.path.exists(os.path.join(models_path, 'entities.py')), "MVC falhou: entities.py não existe"
    
    # View
    templates_path = os.path.join(app_path, 'templates')
    assert os.path.exists(templates_path), "MVC falhou: diretório templates não existe"
    
    # Controller
    controllers_path = os.path.join(app_path, 'controllers')
    assert os.path.exists(controllers_path), "MVC falhou: diretório controllers não existe"
    
    # Repository (camada adicional)
    repositories_path = os.path.join(app_path, 'repositories')
    assert os.path.exists(repositories_path), "MVC falhou: diretório repositories não existe"
    
    print("✅ MVC funcionando corretamente - separação de camadas implementada")

def run_all_tests():
    """Executa todos os testes"""
    print("🧪 INICIANDO TESTES DOS PADRÕES DE PROJETO")
    print("=" * 50)
    
    try:
        test_singleton()
        test_factory()
        test_observer()
        test_strategy()
        test_repository()
        test_mvc_separation()
        
        print("\n" + "=" * 50)
        print("🎉 TODOS OS TESTES PASSARAM COM SUCESSO!")
        print("✅ Singleton: Instância única garantida")
        print("✅ Factory Method: Criação padronizada de objetos")
        print("✅ Observer: Sistema de notificações funcionando")
        print("✅ Strategy: Algoritmos intercambiáveis implementados")
        print("✅ Repository: Abstração de dados funcionando")
        print("✅ MVC: Separação de camadas correta")
        print("\n🏆 Sistema implementa corretamente todos os padrões!")
        
    except AssertionError as e:
        print(f"\n❌ TESTE FALHOU: {e}")
        return False
    except Exception as e:
        print(f"\n💥 ERRO INESPERADO: {e}")
        return False
    
    return True

if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)