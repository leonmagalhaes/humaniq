import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import Layout from '../components/Layout';
import Card from '../components/Card';
import Button from '../components/Button';
import api from '../services/api';

interface Challenge {
  id: number;
  title: string;
  description: string;
  videoUrl: string;
  completed: boolean;
  dueDate: string;
  practicalChallenge: string;
}

interface Question {
  id: number;
  text: string;
  options: string[];
  correctOption: number;
}

const Challenge: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  
  const [challenge, setChallenge] = useState<Challenge | null>(null);
  const [questions, setQuestions] = useState<Question[]>([]);
  const [answers, setAnswers] = useState<Record<number, number>>({});
  const [quizSubmitted, setQuizSubmitted] = useState(false);
  const [quizScore, setQuizScore] = useState<number | null>(null);
  const [challengeCompleted, setChallengeCompleted] = useState(false);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  useEffect(() => {
    const fetchChallengeData = async () => {
      setLoading(true);
      try {
        // Buscar dados do desafio
        const challengeResponse = await api.get(`/challenges/${id}`);
        setChallenge(challengeResponse.data);
        setChallengeCompleted(challengeResponse.data.completed);
        
        // Buscar perguntas do quiz
        const questionsResponse = await api.get(`/challenges/${id}/questions`);
        setQuestions(questionsResponse.data);
        
        // Verificar se o quiz já foi respondido
        try {
          const quizResponse = await api.get(`/challenges/${id}/quiz-result`);
          if (quizResponse.data.completed) {
            setQuizSubmitted(true);
            setQuizScore(quizResponse.data.score);
          }
        } catch (error) {
          // Quiz ainda não foi respondido, não é um erro
        }
      } catch (error) {
        console.error('Erro ao carregar dados do desafio:', error);
        setError('Não foi possível carregar os dados do desafio. Tente novamente mais tarde.');
      } finally {
        setLoading(false);
      }
    };
    
    if (id) {
      fetchChallengeData();
    }
  }, [id]);
  
  const handleAnswerSelect = (questionId: number, optionIndex: number) => {
    setAnswers({
      ...answers,
      [questionId]: optionIndex
    });
  };
  
  const handleQuizSubmit = async () => {
    // Verificar se todas as perguntas foram respondidas
    if (Object.keys(answers).length !== questions.length) {
      alert('Por favor, responda todas as perguntas antes de enviar.');
      return;
    }
    
    setSubmitting(true);
    
    try {
      const response = await api.post(`/challenges/${id}/submit-quiz`, { answers });
      setQuizSubmitted(true);
      setQuizScore(response.data.score);
    } catch (error) {
      console.error('Erro ao enviar quiz:', error);
      setError('Não foi possível enviar suas respostas. Tente novamente.');
    } finally {
      setSubmitting(false);
    }
  };
  
  const handleMarkAsCompleted = async () => {
    setSubmitting(true);
    
    try {
      await api.post(`/challenges/${id}/complete`);
      setChallengeCompleted(true);
      
      // Redirecionar para o dashboard após um breve delay
      setTimeout(() => {
        navigate('/dashboard');
      }, 2000);
    } catch (error) {
      console.error('Erro ao marcar desafio como concluído:', error);
      setError('Não foi possível marcar o desafio como concluído. Tente novamente.');
    } finally {
      setSubmitting(false);
    }
  };
  
  if (loading) {
    return (
      <Layout>
        <div className="container mx-auto px-4 py-16 flex items-center justify-center">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-secondary mx-auto mb-4"></div>
            <p className="text-xl">Carregando desafio...</p>
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
  
  if (!challenge) {
    return (
      <Layout>
        <div className="container mx-auto px-4 py-16">
          <Card className="max-w-2xl mx-auto">
            <div className="text-center">
              <h2 className="text-2xl font-bold mb-4">Desafio não encontrado</h2>
              <p className="mb-6">O desafio que você está procurando não existe ou foi removido.</p>
              <Button onClick={() => navigate('/dashboard')}>
                Voltar para o Dashboard
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
        <div className="max-w-4xl mx-auto">
          {/* Cabeçalho do desafio */}
          <div className="mb-8">
            <h1 className="text-3xl font-bold mb-2">{challenge.title}</h1>
            <div className="flex items-center justify-between">
              <p className="text-white text-opacity-70">
                Prazo: {new Date(challenge.dueDate).toLocaleDateString('pt-BR')}
              </p>
              <span className={`px-3 py-1 rounded-full text-sm ${
                challengeCompleted 
                  ? 'bg-green-500 bg-opacity-20 text-green-500' 
                  : 'bg-yellow-500 bg-opacity-20 text-yellow-500'
              }`}>
                {challengeCompleted ? 'Concluído' : 'Em andamento'}
              </span>
            </div>
          </div>
          
          {/* Descrição do desafio */}
          <Card className="mb-8">
            <h2 className="text-xl font-bold mb-4">Sobre este desafio</h2>
            <p className="text-white text-opacity-90 mb-6">
              {challenge.description}
            </p>
          </Card>
          
          {/* Vídeo do desafio */}
          <Card className="mb-8">
            <h2 className="text-xl font-bold mb-4">Vídeo explicativo</h2>
            <div className="aspect-w-16 aspect-h-9 mb-4">
              <iframe
                src={challenge.videoUrl}
                title="Vídeo do desafio"
                frameBorder="0"
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                allowFullScreen
                className="w-full h-64 md:h-96 rounded-lg"
              ></iframe>
            </div>
          </Card>
          
          {/* Quiz */}
          <Card className="mb-8">
            <h2 className="text-xl font-bold mb-6">Quiz de compreensão</h2>
            
            {quizSubmitted ? (
              <div>
                <div className={`p-4 rounded-lg mb-6 ${
                  quizScore && quizScore >= 2 
                    ? 'bg-green-500 bg-opacity-20' 
                    : 'bg-red-500 bg-opacity-20'
                }`}>
                  <p className="font-medium">
                    {quizScore && quizScore >= 2 
                      ? `Parabéns! Você acertou ${quizScore} de ${questions.length} questões.` 
                      : `Você acertou ${quizScore} de ${questions.length} questões. Reveja o conteúdo e tente novamente.`}
                  </p>
                </div>
                
                {questions.map((question, index) => (
                  <div key={question.id} className="mb-6">
                    <p className="font-medium mb-3">
                      {index + 1}. {question.text}
                    </p>
                    
                    <div className="space-y-2">
                      {question.options.map((option, optIndex) => (
                        <div 
                          key={optIndex}
                          className={`p-3 rounded-lg ${
                            answers[question.id] === optIndex && question.correctOption === optIndex
                              ? 'bg-green-500 bg-opacity-20'
                              : answers[question.id] === optIndex && question.correctOption !== optIndex
                                ? 'bg-red-500 bg-opacity-20'
                                : question.correctOption === optIndex
                                  ? 'bg-green-500 bg-opacity-10'
                                  : 'bg-white bg-opacity-5'
                          }`}
                        >
                          {option}
                        </div>
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div>
                {questions.map((question, index) => (
                  <div key={question.id} className="mb-6">
                    <p className="font-medium mb-3">
                      {index + 1}. {question.text}
                    </p>
                    
                    <div className="space-y-2">
                      {question.options.map((option, optIndex) => (
                        <button
                          key={optIndex}
                          onClick={() => handleAnswerSelect(question.id, optIndex)}
                          className={`w-full p-3 text-left rounded-lg transition-all ${
                            answers[question.id] === optIndex
                              ? 'bg-secondary bg-opacity-30'
                              : 'bg-white bg-opacity-5 hover:bg-opacity-10'
                          }`}
                        >
                          {option}
                        </button>
                      ))}
                    </div>
                  </div>
                ))}
                
                <Button
                  onClick={handleQuizSubmit}
                  disabled={Object.keys(answers).length !== questions.length || submitting}
                  fullWidth
                >
                  {submitting ? 'Enviando...' : 'Enviar respostas'}
                </Button>
              </div>
            )}
          </Card>
          
          {/* Desafio prático */}
          <Card className="mb-8">
            <h2 className="text-xl font-bold mb-4">Desafio prático</h2>
            <p className="text-white text-opacity-90 mb-6">
              {challenge.practicalChallenge}
            </p>
          </Card>
          
          {/* Botão de conclusão */}
          {!challengeCompleted && quizSubmitted && (
            <div className="text-center">
              <Button
                onClick={handleMarkAsCompleted}
                disabled={submitting}
                className="px-8 py-3"
              >
                {submitting ? 'Processando...' : 'Marcar desafio como concluído'}
              </Button>
              <p className="text-sm text-white text-opacity-70 mt-2">
                Ao marcar como concluído, você confirma que realizou o desafio prático.
              </p>
            </div>
          )}
          
          {challengeCompleted && (
            <div className="text-center">
              <div className="bg-green-500 bg-opacity-20 text-green-500 p-4 rounded-lg mb-4">
                <p className="font-medium">
                  Parabéns! Você concluiu este desafio com sucesso.
                </p>
              </div>
              <Button
                onClick={() => navigate('/dashboard')}
                variant="outline"
              >
                Voltar para o Dashboard
              </Button>
            </div>
          )}
        </div>
      </div>
    </Layout>
  );
};

export default Challenge;
