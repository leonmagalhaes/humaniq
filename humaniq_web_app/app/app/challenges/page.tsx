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
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";

export default function Challenges() {
  const [activeChallenge, setActiveChallenge] = useState<number | null>(0);

  const challenges = [
    {
      title: "Active Listening Master",
      description: "Practice active listening techniques in your daily conversations",
      duration: "7 days",
      points: 500,
      progress: 65,
      tasks: [
        "Practice mirroring in 3 conversations",
        "Ask open-ended questions",
        "Summarize what others say",
        "Maintain eye contact",
      ]
    },
    {
      title: "Public Speaking Pro",
      description: "Improve your presentation skills through daily exercises",
      duration: "5 days",
      points: 400,
      progress: 0,
      tasks: [
        "Record a 2-minute speech",
        "Practice body language",
        "Work on voice modulation",
        "Give a presentation to friends",
      ]
    },
    {
      title: "Empathy Builder",
      description: "Develop stronger emotional intelligence",
      duration: "10 days",
      points: 600,
      progress: 0,
      tasks: [
        "Journal about others' perspectives",
        "Practice active empathy",
        "Identify emotions in others",
        "Respond with understanding",
      ]
    }
  ];

  return (
    <div className="min-h-screen bg-background p-8">
      <div className="max-w-4xl mx-auto space-y-8">
        <div className="text-center space-y-4">
          <h1 className="text-4xl font-bold gradient-text">Weekly Challenges</h1>
          <p className="text-muted-foreground">
            Complete challenges to earn points and develop your skills
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {challenges.map((challenge, index) => (
            <Card
              key={index}
              className={`card-hover ${
                activeChallenge === index ? "gradient-border" : ""
              }`}
            >
              <CardHeader>
                <div className="flex justify-between items-start">
                  <CardTitle>{challenge.title}</CardTitle>
                  <Badge variant="outline" className="bg-primary/20">
                    {challenge.points} pts
                  </Badge>
                </div>
                <CardDescription>{challenge.description}</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <div className="flex justify-between mb-2">
                    <span className="text-sm text-muted-foreground">Progress</span>
                    <span className="text-sm">{challenge.progress}%</span>
                  </div>
                  <Progress value={challenge.progress} className="h-2" />
                </div>
                <div className="space-y-2">
                  {challenge.tasks.map((task, taskIndex) => (
                    <div
                      key={taskIndex}
                      className="flex items-center gap-2 text-sm"
                    >
                      <div className="w-2 h-2 rounded-full bg-primary" />
                      <span>{task}</span>
                    </div>
                  ))}
                </div>
                <Button
                  className="w-full bg-gradient-to-r from-primary to-secondary"
                  onClick={() => setActiveChallenge(index)}
                >
                  {challenge.progress > 0 ? "Continue Challenge" : "Start Challenge"}
                </Button>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </div>
  );
}