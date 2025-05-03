"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group";
import { Label } from "@/components/ui/label";
import { useToast } from "@/components/ui/use-toast";

export default function InitialTest() {
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [answers, setAnswers] = useState<string[]>([]);
  const { toast } = useToast();

  const questions = [
    {
      question: "How do you typically handle conflicts in a team?",
      options: [
        "I prefer to avoid confrontation",
        "I try to find a compromise",
        "I assert my position firmly",
        "I collaborate to find the best solution"
      ]
    },
    {
      question: "What's your preferred way of learning new skills?",
      options: [
        "Reading and research",
        "Practical exercises",
        "Group discussions",
        "Video tutorials"
      ]
    },
    {
      question: "How do you handle feedback?",
      options: [
        "I actively seek it out",
        "I accept it when given",
        "I prefer not to receive it",
        "I analyze it thoroughly"
      ]
    },
    {
      question: "What motivates you the most?",
      options: [
        "Personal achievement",
        "Recognition from others",
        "Learning new things",
        "Helping others succeed"
      ]
    },
    {
      question: "How do you prefer to communicate in professional settings?",
      options: [
        "Written communication",
        "Face-to-face meetings",
        "Group discussions",
        "Visual presentations"
      ]
    }
  ];

  const handleAnswer = (answer: string) => {
    const newAnswers = [...answers];
    newAnswers[currentQuestion] = answer;
    setAnswers(newAnswers);
  };

  const handleNext = () => {
    if (!answers[currentQuestion]) {
      toast({
        title: "Please select an answer",
        variant: "destructive",
      });
      return;
    }
    if (currentQuestion < questions.length - 1) {
      setCurrentQuestion(currentQuestion + 1);
    } else {
      // Submit test
      toast({
        title: "Test completed!",
        description: "Your personalized learning path is being created.",
      });
      // Redirect to dashboard after submission
      window.location.href = "/dashboard";
    }
  };

  return (
    <div className="min-h-screen bg-background p-8">
      <div className="max-w-2xl mx-auto space-y-8">
        <div className="text-center space-y-4">
          <h1 className="text-4xl font-bold gradient-text">Initial Assessment</h1>
          <p className="text-muted-foreground">
            Help us understand your current skills and preferences
          </p>
        </div>

        <Progress
          value={(currentQuestion / questions.length) * 100}
          className="h-2"
        />

        <Card className="card-hover">
          <CardHeader>
            <CardTitle>Question {currentQuestion + 1}</CardTitle>
            <CardDescription>
              {questions[currentQuestion].question}
            </CardDescription>
          </CardHeader>
          <CardContent>
            <RadioGroup
              onValueChange={handleAnswer}
              value={answers[currentQuestion]}
              className="space-y-4"
            >
              {questions[currentQuestion].options.map((option, index) => (
                <div key={index} className="flex items-center space-x-2">
                  <RadioGroupItem value={option} id={`option-${index}`} />
                  <Label htmlFor={`option-${index}`}>{option}</Label>
                </div>
              ))}
            </RadioGroup>
          </CardContent>
        </Card>

        <div className="flex justify-end">
          <Button
            onClick={handleNext}
            className="bg-gradient-to-r from-primary to-secondary"
          >
            {currentQuestion < questions.length - 1 ? "Next Question" : "Complete Test"}
          </Button>
        </div>
      </div>
    </div>
  );
}