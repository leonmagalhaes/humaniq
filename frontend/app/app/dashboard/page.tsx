"use client";

import { useEffect, useState } from "react";
import Image from "next/image";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { useAuthContext } from "@/components/auth-provider";
import { challenges, forum, badges } from "@/lib/api";
import type { Challenge, ForumPost, UserBadge } from "@/lib/types";

export default function Dashboard() {
  const { user } = useAuthContext();
  const [userChallenges, setUserChallenges] = useState<Challenge[]>([]);
  const [userBadges, setUserBadges] = useState<UserBadge[]>([]);
  const [forumPosts, setForumPosts] = useState<ForumPost[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        const [challengesData, badgesData, postsData] = await Promise.all([
          challenges.getAll(),
          badges.getUserBadges(),
          forum.getPosts(),
        ]);

        setUserChallenges(challengesData);
        setUserBadges(badgesData);
        setForumPosts(postsData);
      } catch (error) {
        console.error("Error fetching dashboard data:", error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchDashboardData();
  }, []);

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center space-y-4">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
          <p className="text-muted-foreground">Loading your dashboard...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background">
      <nav className="border-b border-border p-4">
        <div className="container mx-auto flex justify-between items-center">
          <div className="flex items-center gap-2">
            <Image
              src="/Humaniq App.png"
              alt="HUMANIQ Logo"
              width={40}
              height={40}
              className="rounded-full"
            />
            <span className="text-xl font-bold gradient-text">HUMANIQ</span>
          </div>
          <div className="flex items-center gap-4">
            <Link href="/profile">
              <Button variant="ghost">Profile</Button>
            </Link>
            <Link href="/logout">
              <Button variant="outline">Logout</Button>
            </Link>
          </div>
        </div>
      </nav>

      <main className="container mx-auto p-4 space-y-8">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <Card className="col-span-2">
            <CardHeader>
              <CardTitle>Welcome back, {user?.name}!</CardTitle>
              <CardDescription>
                Track your progress and complete challenges to level up your skills
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div>
                  <div className="flex justify-between mb-2">
                    <span>Level Progress</span>
                    <span>{user?.level}</span>
                  </div>
                  <Progress value={(user?.points ?? 0) % 1000 / 10} className="h-2" />
                </div>
                <div className="flex gap-2">
                  <Badge variant="outline" className="bg-primary/20">
                    Level {user?.level}
                  </Badge>
                  <Badge variant="outline" className="bg-secondary/20">
                    {user?.points} Points
                  </Badge>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Latest Challenge</CardTitle>
              <CardDescription>Complete to earn bonus points</CardDescription>
            </CardHeader>
            <CardContent>
              {userChallenges[0] && (
                <div className="space-y-4">
                  <h4 className="font-semibold">{userChallenges[0].title}</h4>
                  <p className="text-sm text-muted-foreground">
                    {userChallenges[0].description}
                  </p>
                  <Link href={`/challenges/${userChallenges[0].id}`}>
                    <Button className="w-full bg-gradient-to-r from-primary to-secondary">
                      Start Challenge
                    </Button>
                  </Link>
                </div>
              )}
            </CardContent>
          </Card>
        </div>

        <Tabs defaultValue="challenges">
          <TabsList className="grid w-full grid-cols-3 max-w-[400px]">
            <TabsTrigger value="challenges">Challenges</TabsTrigger>
            <TabsTrigger value="badges">Badges</TabsTrigger>
            <TabsTrigger value="forum">Forum</TabsTrigger>
          </TabsList>

          <TabsContent value="challenges" className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {userChallenges.map((challenge) => (
                <Card key={challenge.id} className="card-hover">
                  <CardHeader>
                    <CardTitle>{challenge.title}</CardTitle>
                    <CardDescription>{challenge.description}</CardDescription>
                  </CardHeader>
                  <CardContent>
                    <Link href={`/challenges/${challenge.id}`}>
                      <Button variant="outline" className="w-full">
                        View Challenge
                      </Button>
                    </Link>
                  </CardContent>
                </Card>
              ))}
            </div>
          </TabsContent>

          <TabsContent value="badges" className="space-y-4">
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              {userBadges.map((badge) => (
                <Card key={badge.id} className="text-center p-4">
                  <Image
                    src={badge.image_url}
                    alt={badge.name}
                    width={64}
                    height={64}
                    className="mx-auto mb-4"
                  />
                  <h4 className="font-semibold">{badge.name}</h4>
                  <p className="text-sm text-muted-foreground">
                    {badge.description}
                  </p>
                </Card>
              ))}
            </div>
          </TabsContent>

          <TabsContent value="forum" className="space-y-4">
            <Card>
              <CardHeader>
                <CardTitle>Recent Discussions</CardTitle>
                <CardDescription>
                  Join the conversation with other learners
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {forumPosts.map((post) => (
                    <div
                      key={post.id}
                      className="p-4 border border-border rounded-lg"
                    >
                      <div className="flex items-center gap-2 mb-2">
                        <div className="w-8 h-8 rounded-full bg-primary/20" />
                        <div>
                          <p className="font-semibold">{post.user?.name}</p>
                          <p className="text-sm text-muted-foreground">
                            {new Date(post.created_at).toLocaleDateString()}
                          </p>
                        </div>
                      </div>
                      <h4 className="font-semibold mb-2">{post.title}</h4>
                      <p className="text-muted-foreground">{post.content}</p>
                      <div className="mt-4">
                        <Link href={`/forum/posts/${post.id}`}>
                          <Button variant="outline" size="sm">
                            View Discussion
                          </Button>
                        </Link>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </main>
    </div>
  );
}