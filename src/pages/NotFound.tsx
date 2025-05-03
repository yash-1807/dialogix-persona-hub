
import { useEffect } from "react";
import { useLocation, Link } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Home } from "lucide-react";

const NotFound = () => {
  const location = useLocation();

  useEffect(() => {
    console.error(
      "404 Error: User attempted to access non-existent route:",
      location.pathname
    );
  }, [location.pathname]);

  return (
    <div className="min-h-screen flex items-center justify-center bg-background">
      <div className="text-center px-4">
        <h1 className="text-7xl font-bold mb-4 text-primary">404</h1>
        <div className="mb-6">
          <p className="text-2xl font-semibold mb-2">Page not found</p>
          <p className="text-muted-foreground">
            The persona you're looking for seems to have wandered off...
          </p>
        </div>
        <Button asChild>
          <Link to="/">
            <Home className="mr-2 h-4 w-4" /> 
            Return Home
          </Link>
        </Button>
      </div>
    </div>
  );
};

export default NotFound;
