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
  name: z.string().min(2, "Name must be at least 2 characters"),
  email: z.string().email("Invalid email address"),
  password: z.string().min(8, "Password must be at least 8 characters"),
  confirmPassword: z.string(),
}).refine((data) => data.password === data.confirmPassword, {
  message: "Passwords don't match",
  path: ["confirmPassword"],
});

export default function Register() {
  const { toast } = useToast();
  const { register } = useAuth();
  const [isLoading, setIsLoading] = useState(false);

  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      name: "",
      email: "",
      password: "",
      confirmPassword: "",
    },
  });

  async function onSubmit(values: z.infer<typeof formSchema>) {
    setIsLoading(true);
    try {
      await register(values.name, values.email, values.password);
      toast({
        title: "Registration successful!",
        description: "Welcome to HUMANIQ!",
      });
    } catch (error) {
      toast({
        variant: "destructive",
        title: "Error",
        description: "Registration failed. Please try again.",
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
              Create Your Account
            </h2>
            <p className="mt-2 text-sm text-muted-foreground">
              Join HUMANIQ and start your personal development journey
            </p>
          </div>

          <Form {...form}>
            <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
              <FormField
                control={form.control}
                name="name"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Name</FormLabel>
                    <FormControl>
                      <Input placeholder="John Doe" {...field} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />

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

              <FormField
                control={form.control}
                name="confirmPassword"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Confirm Password</FormLabel>
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
                {isLoading ? "Creating account..." : "Create Account"}
              </Button>
            </form>
          </Form>

          <p className="text-center text-sm text-muted-foreground">
            Already have an account?{" "}
            <Link href="/login" className="text-primary hover:underline">
              Login here
            </Link>
          </p>
        </div>
      </div>

      <div className="hidden md:flex flex-1 bg-muted items-center justify-center p-8">
        <div className="max-w-md text-center space-y-6">
          <h3 className="text-2xl font-bold gradient-text">
            Welcome to HUMANIQ
          </h3>
          <p className="text-muted-foreground">
            Join our community of young professionals developing their human skills
            through engaging challenges and personalized learning paths.
          </p>
        </div>
      </div>
    </div>
  );
}