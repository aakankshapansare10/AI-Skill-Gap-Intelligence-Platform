import { useState } from "react";
import { Link } from "react-router-dom";
import { Sparkles, Menu, X } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";

function Navbar() {
  const [isOpen, setIsOpen] = useState(false);

  const closeMenu = () => {
    setIsOpen(false);
  };

  return (
    <nav className="sticky top-0 z-50 border-b border-gray-100 bg-white/90 backdrop-blur-md">
      <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-4">

        {/* Logo */}
        <Link
          to="/"
          onClick={closeMenu}
          className="flex items-center gap-2"
        >
          <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-indigo-600 text-white">
            <Sparkles size={18} />
          </div>

          <span className="text-xl font-bold tracking-tight">
            Career<span className="text-indigo-600">Genome</span>
          </span>
        </Link>

        {/* Desktop Navigation */}
        <div className="hidden items-center gap-8 md:flex">
          <Link
            to="/"
            className="text-sm font-medium text-gray-600 transition hover:text-indigo-600"
          >
            Home
          </Link>

          <Link
            to="/analyze"
            className="text-sm font-medium text-gray-600 transition hover:text-indigo-600"
          >
            Analyze Resume
          </Link>

          <Link
            to="/dashboard"
            className="text-sm font-medium text-gray-600 transition hover:text-indigo-600"
          >
            Dashboard
          </Link>
        </div>

        {/* Desktop CTA */}
        <Link
          to="/analyze"
          className="hidden rounded-xl bg-indigo-600 px-5 py-2.5 text-sm font-semibold text-white shadow-sm transition hover:bg-indigo-700 hover:shadow-md md:block"
        >
          Get Started
        </Link>

        {/* Mobile Menu Button */}
        <button
          type="button"
          onClick={() => setIsOpen(!isOpen)}
          className="rounded-lg p-2 text-gray-700 transition hover:bg-gray-100 md:hidden"
          aria-label="Toggle menu"
        >
          {isOpen ? <X size={24} /> : <Menu size={24} />}
        </button>
      </div>

      {/* Mobile Menu */}
      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: "auto" }}
            exit={{ opacity: 0, height: 0 }}
            transition={{ duration: 0.25 }}
            className="overflow-hidden border-t border-gray-100 bg-white md:hidden"
          >
            <div className="flex flex-col gap-2 px-6 py-5">

              <Link
                to="/"
                onClick={closeMenu}
                className="rounded-xl px-4 py-3 text-sm font-medium text-gray-700 transition hover:bg-indigo-50 hover:text-indigo-600"
              >
                Home
              </Link>

              <Link
                to="/analyze"
                onClick={closeMenu}
                className="rounded-xl px-4 py-3 text-sm font-medium text-gray-700 transition hover:bg-indigo-50 hover:text-indigo-600"
              >
                Analyze Resume
              </Link>

              <Link
                to="/dashboard"
                onClick={closeMenu}
                className="rounded-xl px-4 py-3 text-sm font-medium text-gray-700 transition hover:bg-indigo-50 hover:text-indigo-600"
              >
                Dashboard
              </Link>

              <Link
                to="/analyze"
                onClick={closeMenu}
                className="mt-2 rounded-xl bg-indigo-600 px-4 py-3 text-center text-sm font-semibold text-white transition hover:bg-indigo-700"
              >
                Get Started
              </Link>

            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </nav>
  );
}

export default Navbar;