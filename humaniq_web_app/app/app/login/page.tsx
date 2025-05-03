"use client";

import { useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import * as z from "zod";
import Link from "next/link";
import Image from "next/image";
import { Button } from "@/components/ui/button";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { useToast } from "@/components/ui/use-toast";
import { useAuth } from "@/hooks/useAuth";

const formSchema = z.object({
  email: z.string().email("Invalid email address"),
  password: z.string().min(1, "Password is required"),
});

export default function Login() {
  const { toast } = useToast();
  const { login } = useAuth();
  const [isLoading, setIsLoading] = useState(false);

  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      email: "",
      password: "",
    },
  });

  async function onSubmit(values: z.infer<typeof formSchema>) {
    setIsLoading(true);
    try {
      await login(values.email, values.password);
      toast({
        title: "Login successful!",
        description: "Welcome back to HUMANIQ!",
      });
    } catch (error) {
      toast({
        variant: "destructive",
        title: "Error",
        description: "Invalid email or password.",
      });
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <div className="min-h-screen flex flex-col md:flex-row">
      <div className="flex-1 p-8 flex flex-col justify-center items-center">
        <div className="w-full max-w-md space-y-8">
          <div className="flex flex-col items-center">
            <Image
              src="/Humaniq App.png"
              alt="HUMANIQ Logo"
              width={64}
              height={64}
              className="rounded-full"
            />
            <h2 className="mt-6 text-3xl font-bold gradient-text">
              Welcome Back
            </h2>
            <p className="mt-2 text-sm text-muted-foreground">
              Sign in to continue your journey
            </p>
          </div>

          <Form {...form}>
            <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
              <FormField
                control={form.control}
                name="email"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Email</FormLabel>
                    <FormControl>
                      <Input placeholder="john@example.com" type="email" {...field} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <FormField
                control={form.control}
                name="password"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Password</FormLabel>
                    <FormControl>
                      <Input placeholder="********" type="password" {...field} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <Button
                type="submit"
                className="w-full bg-gradient-to-r from-primary to-secondary"
                disabled={isLoading}
              >
                {isLoading ? "Signing in..." : "Sign In"}
              </Button>
            </form>
          </Form>

          <div className="space-y-4">
            <p className="text-center text-sm text-muted-foreground">
              Don't have an account?{" "}
              <Link href="/register" className="text-primary hover:underline">
                Register here
              </Link>
            </p>
            <p className="text-center text-sm">
              <Link href="/forgot-password" className="text-primary hover:underline">
                Forgot your password?
              </Link>
            </p>
          </div>
        </div>
      </div>

      <div className="hidden md:flex flex-1 bg-muted items-center justify-center p-8">
        <div className="max-w-md text-center space-y-6">
          <h3 className="text-2xl font-bold gradient-text">
            Continue Your Growth
          </h3>
          <p className="text-muted-foreground">
            Access your personalized learning path, track your progress, and connect
            with the HUMANIQ community.
          </p>
        </div>
      </div>
    </div>
  );
}