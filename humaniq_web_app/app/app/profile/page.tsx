"use client";

import { useState } from "react";
import Image from "next/image";
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
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";

export default function Profile() {
  const [level] = useState(5);
  const [totalPoints] = useState(2500);
  const [completedChallenges] = useState(12);

  const achievements = [
    {
      icon: "🌟",
      title: "First Steps",
      description: "Completed first module",
      date: "Jan 15, 2024"
    },
    {
      icon: "🎯",
      title: "Goal Setter",
      description: "Set 5 learning goals",
      date: "Jan 20, 2024"
    },
    {
      icon: "🏆",
      title: "Challenge Champion",
      description: "Completed 10 challenges",
      date: "Feb 1, 2024"
    },
    {
      icon: "💪",
      title: "Consistency King",
      description: "30-day streak",
      date: "Feb 15, 2024"
    },
    {
      icon: "🌈",
      title: "Team Player",
      description: "Helped 5 community members",
      date: "Feb 28, 2024"
    },
    {
      icon: "📚",
      title: "Knowledge Seeker",
      description: "Completed all basic modules",
      date: "Mar 5, 2024"
    }
  ];

  const skills = [
    { name: "Communication", level: 80 },
    { name: "Leadership", level: 65 },
    { name: "Problem Solving", level: 75 },
    { name: "Emotional Intelligence", level: 70 },
    { name: "Team Collaboration", level: 85 }
  ];

  return (
    <div className="min-h-screen bg-background p-8">
      <div className="max-w-4xl mx-auto space-y-8">
        <Card>
          <CardContent className="p-6">
            <div className="flex flex-col md:flex-row items-center gap-6">
              <div className="relative">
                <div className="w-32 h-32 rounded-full overflow-hidden">
                  <Image
                    src="/Humaniq App.png"
                    alt="Profile"
                    width={128}
                    height={128}
                    className="object-cover"
                  />
                </div>
                <Button
                  variant="outline"
                  size="sm"
                  className="absolute bottom-0 right-0"
                >
                  Edit
                </Button>
              </div>
              <div className="flex-1 text-center md:text-left">
                <h1 className="text-3xl font-bold mb-2">John Doe</h1>
                <p className="text-muted-foreground mb-4">
                  Aspiring leader | Continuous learner
                </p>
                <div className="flex flex-wrap gap-2">
                  <Badge variant="outline" className="bg-primary/20">
                    Level {level}
                  </Badge>
                  <Badge variant="outline" className="bg-secondary/20">
                    {totalPoints} Points
                  </Badge>
                  <Badge variant="outline">
                    {completedChallenges} Challenges
                  </Badge>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        <Tabs defaultValue="skills">
          <TabsList className="grid w-full grid-cols-2 max-w-[400px]">
            <TabsTrigger value="skills">Skills</TabsTrigger>
            <TabsTrigger value="achievements">Achievements</TabsTrigger>
          </TabsList>

          <TabsContent value="skills" className="space-y-4">
            <Card>
              <CardHeader>
                <CardTitle>Skill Progress</CardTitle>
                <CardDescription>
                  Track your development in key areas
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-6">
                {skills.map((skill, index) => (
                  <div key={index}>
                    <div className="flex justify-between mb-2">
                      <span>{skill.name}</span>
                      <span>{skill.level}%</span>
                    </div>
                    <Progress value={skill.level} className="h-2" />
                  </div>
                ))}
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="achievements" className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {achievements.map((achievement, index) => (
                <Card key={index} className="card-hover">
                  <CardContent className="p-4 flex items-center gap-4">
                    <div className="text-4xl">{achievement.icon}</div>
                    <div>
                      <h3 className="font-semibold">{achievement.title}</h3>
                      <p className="text-sm text-muted-foreground">
                        {achievement.description}
                      </p>
                      <p className="text-xs text-muted-foreground mt-1">
                        Earned on {achievement.date}
                      </p>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
}