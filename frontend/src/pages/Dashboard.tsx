import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import Layout from '../components/Layout';
import Card from '../components/Card';
import Button from '../components/Button';
import api from '../services/api';

interface Challenge {
  id: number;
  title: string;
  description: string;
  completed: boolean;
  dueDate: string;
}

interface Progress {
  completedChallenges: number;
  totalChallenges: number;
  streak: number;
  level: number;
  xp: number;
  nextLevelXp: number;
}

const Dashboard: React.FC = () => {
  const [weeklyChallenge, setWeeklyChallenge] = useState<Challenge | null>(null);
  const [recentChallenges, setRecentChallenges] = useState<Challenge[]>([]);
  const [progress, setProgress] = useState<Progress | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  
  useEffect(() => {
    const fetchDashboardData = async () => {
      setLoading(true);
      try {
        // Buscar desafio da semana
        const challengeResponse = await api.get('/challenges/weekly');
        setWeeklyChallenge(challengeResponse.data);
        
        // Buscar desafios recentes
        const recentResponse = await api.get('/challenges/recent');
        setRecentChallenges(recentResponse.data);
        
        // Buscar progresso
        const progressResponse = await api.get('/users/progress');
        setProgress(progressResponse.data);
      } catch (error) {
        console.error('Erro ao carregar dados do dashboard:', error);
        setError('Não foi possível carregar os dados. Tente novamente mais tarde.');
      } finally {
        setLoading(false);
      }
    };
    
    fetchDashboardData();
  }, []);
  
  if (loading) {
    return (
      <Layout>
        <div className="container mx-auto px-4 py-16 flex items-center justify-center">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-secondary mx-auto mb-4"></div>
            <p className="text-xl">Carregando seu dashboard...</p>
          </div>
        </div>
      </Layout>
    );
  }
  
  if (error) {
    return (
      <Layout>
        <div className="container mx-auto px-4 py-16">
          <Card className="max-w-2xl mx-auto">
            <div className="text-center">
              <h2 className="text-2xl font-bold mb-4 text-red-500">Erro</h2>
              <p className="mb-6">{error}</p>
              <Button onClick={() => window.location.reload()}>
                Tentar novamente
              </Button>
            </div>
          </Card>
        </div>
      </Layout>
    );
  }
  
  return (
    <Layout>
      <div className="container mx-auto px-4 py-12">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Coluna principal */}
          <div className="lg:col-span-2">
            <h1 className="text-3xl font-bold mb-8">Seu Dashboard</h1>
            
            {/* Desafio da semana */}
            {weeklyChallenge && (
              <Card className="mb-8 border-l-4 border-secondary">
                <div className="flex justify-between items-start mb-4">
                  <h2 className="text-2xl font-bold">Desafio da Semana</h2>
                  <span className="bg-secondary bg-opacity-20 text-secondary px-3 py-1 rounded-full text-sm">
                    {weeklyChallenge.completed ? 'Concluído' : 'Em andamento'}
                  </span>
                </div>
                
                <h3 className="text-xl font-medium mb-2">{weeklyChallenge.title}</h3>
                <p className="text-white text-opacity-80 mb-6">
                  {weeklyChallenge.description}
                </p>
                
                <div className="flex justify-between items-center">
                  <span className="text-sm text-white text-opacity-70">
                    Prazo: {new Date(weeklyChallenge.dueDate).toLocaleDateString('pt-BR')}
                  </span>
                  
                  <Link to={`/desafio/${weeklyChallenge.id}`}>
                    <Button>
                      {weeklyChallenge.completed ? 'Ver detalhes' : 'Iniciar desafio'}
                    </Button>
                  </Link>
                </div>
              </Card>
            )}
            
            {/* Desafios recentes */}
            <div className="mb-8">
              <h2 className="text-2xl font-bold mb-4">Desafios Recentes</h2>
              
              {recentChallenges.length > 0 ? (
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {recentChallenges.map((challenge) => (
                    <Card 
                      key={challenge.id} 
                      className={`hover:transform hover:-translate-y-1 transition-all ${
                        challenge.completed ? 'border-l-4 border-green-500' : ''
                      }`}
                      hoverable
                    >
                      <Link to={`/desafio/${challenge.id}`} className="block">
                        <h3 className="text-lg font-medium mb-2">{challenge.title}</h3>
                        <p className="text-white text-opacity-70 text-sm mb-4 line-clamp-2">
                          {challenge.description}
                        </p>
                        
                        <div className="flex justify-between items-center">
                          <span className="text-xs text-white text-opacity-60">
                            {new Date(challenge.dueDate).toLocaleDateString('pt-BR')}
                          </span>
                          
                          <span className={`px-2 py-1 rounded-full text-xs ${
                            challenge.completed 
                              ? 'bg-green-500 bg-opacity-20 text-green-500' 
                              : 'bg-yellow-500 bg-opacity-20 text-yellow-500'
                          }`}>
                            {challenge.completed ? 'Concluído' : 'Pendente'}
                          </span>
                        </div>
                      </Link>
                    </Card>
                  ))}
                </div>
              ) : (
                <Card>
                  <p className="text-center text-white text-opacity-70">
                    Você ainda não tem desafios recentes.
                  </p>
                </Card>
              )}
            </div>
          </div>
          
          {/* Barra lateral */}
          <div>
            {/* Progresso */}
            {progress && (
              <Card className="mb-8">
                <h2 className="text-xl font-bold mb-4">Seu Progresso</h2>
                
                <div className="mb-6">
                  <div className="flex justify-between items-center mb-2">
                    <span className="text-sm">Nível {progress.level}</span>
                    <span className="text-sm">{progress.xp}/{progress.nextLevelXp} XP</span>
                  </div>
                  <div className="w-full bg-white bg-opacity-10 rounded-full h-2">
                    <div 
                      className="bg-secondary h-2 rounded-full" 
                      style={{ width: `${(progress.xp / progress.nextLevelXp) * 100}%` }}
                    ></div>
                  </div>
                </div>
                
                <div className="grid grid-cols-2 gap-4 mb-6">
                  <div className="bg-white bg-opacity-5 rounded-lg p-4 text-center">
                    <span className="block text-2xl font-bold text-secondary mb-1">
                      {progress.completedChallenges}
                    </span>
                    <span className="text-sm text-white text-opacity-70">
                      Desafios concluídos
                    </span>
                  </div>
                  
                  <div className="bg-white bg-opacity-5 rounded-lg p-4 text-center">
                    <span className="block text-2xl font-bold text-secondary mb-1">
                      {progress.streak}
                    </span>
                    <span className="text-sm text-white text-opacity-70">
                      Dias de sequência
                    </span>
                  </div>
                </div>
                
                <Link to="/perfil" className="block text-center">
                  <Button variant="outline" fullWidth>
                    Ver perfil completo
                  </Button>
                </Link>
              </Card>
            )}
            
            {/* Dicas */}
            <Card>
              <h2 className="text-xl font-bold mb-4">Dicas para o Sucesso</h2>
              
              <ul className="space-y-4">
                <li className="flex items-start">
                  <span className="text-secondary mr-2">•</span>
                  <p className="text-white text-opacity-80">
                    Complete um desafio por semana para manter sua sequência.
                  </p>
                </li>
                <li className="flex items-start">
                  <span className="text-secondary mr-2">•</span>
                  <p className="text-white text-opacity-80">
                    Reflita sobre o que aprendeu após cada desafio.
                  </p>
                </li>
                <li className="flex items-start">
                  <span className="text-secondary mr-2">•</span>
                  <p className="text-white text-opacity-80">
                    Aplique os conhecimentos no seu dia a dia.
                  </p>
                </li>
                <li className="flex items-start">
                  <span className="text-secondary mr-2">•</span>
                  <p className="text-white text-opacity-80">
                    Compartilhe seu progresso com amigos para se manter motivado.
                  </p>
                </li>
              </ul>
            </Card>
          </div>
        </div>
      </div>
    </Layout>
  );
};

export default Dashboard;
