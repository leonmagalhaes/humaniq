import Image from "next/image";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import { motion } from "framer-motion";

export default function Home() {
  return (
    <main className="min-h-screen flex flex-col">
      <nav className="w-full p-4 flex justify-between items-center border-b border-border">
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
        <div className="flex gap-4">
          <Link href="/login">
            <Button variant="ghost">Login</Button>
          </Link>
          <Link href="/register">
            <Button className="bg-gradient-to-r from-primary to-secondary">
              Get Started
            </Button>
          </Link>
        </div>
      </nav>

      <section className="flex-1 container mx-auto px-4 py-16 flex flex-col md:flex-row items-center gap-12">
        <div className="flex-1 space-y-6">
          <h1 className="text-4xl md:text-6xl font-bold">
            Develop Your{" "}
            <span className="gradient-text">Human Skills</span>
          </h1>
          <p className="text-lg text-muted-foreground">
            Join HUMANIQ to enhance your soft skills, earn achievements, and connect
            with like-minded individuals. Perfect for young professionals aged
            15-25.
          </p>
          <div className="flex gap-4">
            <Link href="/register">
              <Button size="lg" className="bg-gradient-to-r from-primary to-secondary">
                Start Your Journey
              </Button>
            </Link>
            <Link href="/about">
              <Button size="lg" variant="outline">
                Learn More
              </Button>
            </Link>
          </div>
        </div>
        <div className="flex-1 relative">
          <Image
            src="/Humaniq App.png"
            alt="HUMANIQ App"
            width={500}
            height={500}
            className="rounded-lg shadow-2xl"
          />
        </div>
      </section>

      <section className="bg-muted py-16">
        <div className="container mx-auto px-4">
          <h2 className="text-3xl font-bold text-center mb-12">
            Why Choose <span className="gradient-text">HUMANIQ</span>?
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {features.map((feature, index) => (
              <div
                key={index}
                className="p-6 rounded-lg bg-card card-hover"
              >
                <h3 className="text-xl font-semibold mb-3">{feature.title}</h3>
                <p className="text-muted-foreground">{feature.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      <footer className="border-t border-border py-8">
        <div className="container mx-auto px-4 text-center text-muted-foreground">
          <p>© 2024 HUMANIQ. All rights reserved.</p>
        </div>
      </footer>
    </main>
  );
}

const features = [
  {
    title: "Personalized Learning",
    description: "Get customized content based on your initial assessment and learning goals.",
  },
  {
    title: "Gamified Experience",
    description: "Earn points, badges, and climb the leaderboard as you develop your skills.",
  },
  {
    title: "Community Support",
    description: "Connect with peers, share experiences, and learn from collective wisdom.",
  },
];