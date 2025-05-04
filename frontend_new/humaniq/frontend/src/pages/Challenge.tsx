import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import Layout from '../components/Layout';
import Card from '../components/Card';
import Button from '../components/Button';
import api from '../services/api';

interface Desafio {
  id: number;
  title: string;
  description: string;
  difficulty: string;
  assessment_id: number;
  created_at: string;
}

const Challenge: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  
  const [desafio, setDesafio] = useState<Desafio | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [answer, setAnswer] = useState('');
  const [submitting, setSubmitting] = useState(false);
  
  useEffect(() => {
    const fetchDesafio = async () => {
      try {
        const response = await api.get(`/api/desafios/${id}`);
        setDesafio(response.data);
      } catch (err) {
        setError('Erro ao carregar desafio');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    
    fetchDesafio();
  }, [id]);
  
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitting(true);
    
    try {
      await api.post(`/api/desafios/${id}/submit`, { answer });
      navigate(`/assessment/${desafio?.assessment_id}`, { 
        state: { message: 'Resposta enviada com sucesso!' } 
      });
    } catch (err) {
      setError('Erro ao enviar resposta');
      console.error(err);
    } finally {
      setSubmitting(false);
    }
  };
  
  if (loading) {
    return (
      <Layout>
        <div className="text-center">
          <p>Carregando...</p>
        </div>
      </Layout>
    );
  }
  
  if (error || !desafio) {
    return (
      <Layout>
        <div className="text-center">
          <p className="text-red-500">{error || 'Desafio não encontrado'}</p>
          <Button onClick={() => navigate('/dashboard')} className="mt-4">
            Voltar para Dashboard
          </Button>
        </div>
      </Layout>
    );
  }
  
  return (
    <Layout>
      <div className="max-w-3xl mx-auto">
        <Card>
          <div className="mb-6">
            <h1 className="text-2xl font-bold mb-2">{desafio.title}</h1>
            <span className={`px-3 py-1 rounded-full text-sm font-medium ${
              desafio.difficulty === 'Easy' ? 'bg-green-100 text-green-800' :
              desafio.difficulty === 'Medium' ? 'bg-yellow-100 text-yellow-800' :
              'bg-red-100 text-red-800'
            }`}>
              {desafio.difficulty}
            </span>
          </div>
          
          <div className="mb-8">
            <h2 className="text-lg font-semibold mb-2">Descrição</h2>
            <div className="bg-gray-50 p-4 rounded-md">
              <p className="whitespace-pre-line">{desafio.description}</p>
            </div>
          </div>
          
          <form onSubmit={handleSubmit}>
            <div className="mb-4">
              <label htmlFor="answer" className="block text-gray-700 font-medium mb-2">
                Sua Resposta
              </label>
              <textarea
                id="answer"
                value={answer}
                onChange={(e) => setAnswer(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                rows={8}
                required
              />
            </div>
            
            <div className="flex justify-between">
              <Button 
                variant="outline" 
                onClick={() => navigate(`/assessment/${desafio.assessment_id}`)}
              >
                Voltar
              </Button>
              <Button 
                type="submit" 
                variant="primary"
                disabled={submitting}
              >
                {submitting ? 'Enviando...' : 'Enviar Resposta'}
              </Button>
            </div>
          </form>
        </Card>
      </div>
    </Layout>
  );
};

export default Challenge;
