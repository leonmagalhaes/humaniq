import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import Layout from '../components/Layout';
import Input from '../components/Input';
import Button from '../components/Button';
import Card from '../components/Card';
import { useAuth } from '../contexts/AuthContext';

const Register: React.FC = () => {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [formErrors, setFormErrors] = useState({
    name: '',
    email: '',
    password: '',
    confirmPassword: ''
  });
  
  const { register, user, loading, error, clearError } = useAuth();
  const navigate = useNavigate();
  
  useEffect(() => {
    // Se o usuário já estiver autenticado, redireciona para o dashboard
    if (user) {
      navigate('/avaliacao-inicial');
    }
  }, [user, navigate]);
  
  const validateForm = () => {
    let valid = true;
    const errors = {
      name: '',
      email: '',
      password: '',
      confirmPassword: ''
    };
    
    // Validação de nome
    if (!name) {
      errors.name = 'O nome é obrigatório';
      valid = false;
    } else if (name.length < 3) {
      errors.name = 'O nome deve ter pelo menos 3 caracteres';
      valid = false;
    }
    
    // Validação de email
    if (!email) {
      errors.email = 'O email é obrigatório';
      valid = false;
    } else if (!/\S+@\S+\.\S+/.test(email)) {
      errors.email = 'Email inválido';
      valid = false;
    }
    
    // Validação de senha
    if (!password) {
      errors.password = 'A senha é obrigatória';
      valid = false;
    } else if (password.length < 6) {
      errors.password = 'A senha deve ter pelo menos 6 caracteres';
      valid = false;
    }
    
    // Validação de confirmação de senha
    if (password !== confirmPassword) {
      errors.confirmPassword = 'As senhas não coincidem';
      valid = false;
    }
    
    setFormErrors(errors);
    return valid;
  };
  
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    clearError();
    
    if (validateForm()) {
      await register(name, email, password);
    }
  };
  
  return (
    <Layout>
      <div className="container mx-auto px-4 py-16">
        <div className="max-w-md mx-auto">
          <Card className="mb-8">
            <h1 className="text-2xl font-bold mb-6 text-center">Criar uma conta no HUMANIQ</h1>
            
            {error && (
              <div className="bg-red-500 bg-opacity-20 border border-red-500 text-red-500 px-4 py-3 rounded mb-6">
                {error}
              </div>
            )}
            
            <form onSubmit={handleSubmit}>
              <Input
                type="text"
                name="name"
                label="Nome completo"
                placeholder="Seu nome completo"
                value={name}
                onChange={(e) => setName(e.target.value)}
                error={formErrors.name}
                required
              />
              
              <Input
                type="email"
                name="email"
                label="Email"
                placeholder="Seu melhor email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                error={formErrors.email}
                required
              />
              
              <Input
                type="password"
                name="password"
                label="Senha"
                placeholder="Crie uma senha forte"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                error={formErrors.password}
                required
              />
              
              <Input
                type="password"
                name="confirmPassword"
                label="Confirmar senha"
                placeholder="Confirme sua senha"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                error={formErrors.confirmPassword}
                required
              />
              
              <div className="mb-6">
                <p className="text-sm text-white text-opacity-70">
                  Ao se cadastrar, você concorda com nossos{' '}
                  <a href="#" className="text-secondary hover:underline">
                    Termos de Uso
                  </a>{' '}
                  e{' '}
                  <a href="#" className="text-secondary hover:underline">
                    Política de Privacidade
                  </a>
                  .
                </p>
              </div>
              
              <Button
                type="submit"
                variant="primary"
                fullWidth
                disabled={loading}
              >
                {loading ? 'Cadastrando...' : 'Criar conta'}
              </Button>
            </form>
          </Card>
          
          <div className="text-center">
            <p className="text-white text-opacity-80">
              Já tem uma conta?{' '}
              <Link to="/login" className="text-secondary hover:underline">
                Faça login
              </Link>
            </p>
          </div>
        </div>
      </div>
    </Layout>
  );
};

export default Register;
