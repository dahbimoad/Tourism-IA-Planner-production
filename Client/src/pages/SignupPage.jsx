import React, { useState, useContext } from "react";
import { useNavigate } from "react-router-dom";
// Import du AuthContext
import { AuthContext } from "../contexts/AuthContext"; // <-- Adapter le chemin

const SignupPage = () => {
  const navigate = useNavigate();

  // On récupère la fonction signup depuis le contexte
  const { signup } = useContext(AuthContext);

  // États locaux (ajout de nom et prenom)
  const [email, setEmail] = useState("");
  const [nom, setNom] = useState("");
  const [prenom, setPrenom] = useState("");
  const [password, setPassword] = useState("");
  const [passwordConfirm, setPasswordConfirm] = useState("");
  const [error, setError] = useState("");

  const handleSignup = async (e) => {
    e.preventDefault();
    setError("");

    // Vérification des mots de passe
    if (password !== passwordConfirm) {
      setError("Passwords do not match");
      return;
    }

    // Appel à la fonction signup du contexte
    const result = await signup({
      nom,
      prenom,
      email,
      password,
    });
    if (result) {
      navigate("/login");
    } else {
      setError("Invalid signup");
    }
  };

  return (
    <section className="bg-white-100 min-h-screen flex box-border justify-center items-center">
      <div className="bg-[#ffffff] rounded-2xl flex max-w-3xl p-5 items-center">
        {/* Left Side */}
        <div className="md:w-1/2 px-8">
          <h2 className="font-bold text-3xl text-[#000000]">Register</h2>
          <p className="text-sm mt-4 text-[#112211]">
            Let's discover your second country,{" "}
            <span className="text-red-500 font-bold">MORO</span>
            <span className="text-green-600 font-bold">CCO.</span>
          </p>
          {error && <p style={{ color: "red" }}>{error}</p>}

          {/* Formulaire modifié */}
          <form onSubmit={handleSignup} className="flex flex-col gap-4">
            <input
              className="p-2 mt-6 rounded border"
              type="email"
              placeholder="Write your email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
            <input
              className="p-2 rounded border"
              type="text"
              placeholder="Write your last name"
              value={nom}
              onChange={(e) => setNom(e.target.value)}
              required
            />
            <input
              className="p-2 rounded border"
              type="text"
              placeholder="Write your first name"
              value={prenom}
              onChange={(e) => setPrenom(e.target.value)}
              required
            />
            <div className="relative">
              <input
                className="p-2 rounded border w-full"
                type="password"
                placeholder="Write your password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </div>
            <div className="relative">
              <input
                className="p-2 rounded border w-full"
                type="password"
                placeholder="Confirm your password"
                value={passwordConfirm}
                onChange={(e) => setPasswordConfirm(e.target.value)}
                required
              />
            </div>

            <button
              className="bg-[#8DD3BB] text-black py-2 rounded hover:scale-105 duration-300 hover:bg-[#14183E] hover:text-[#FFF1DA] font-medium"
              type="submit"
            >
              Sign Up
            </button>
          </form>

          <div className="mt-6 items-center text-gray-100">
            <hr className="border-gray-300" />
            <p className="text-center text-sm text-black font-semibold">OR</p>
            <hr className="border-gray-300" />
          </div>

          <button className="bg-white border py-2 w-full rounded-xl mt-5 flex justify-center items-center text-sm hover:scale-105 duration-300 hover:bg-[#60a8bc4f] font-medium">
            {/* Google icon */}
            <svg
              className="mr-3"
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 48 48"
              width="25px"
            >
              <path
                fill="#FFC107"
                d="M43.611,20.083H42V20H24v8h11.303c-1.649,4.657-6.08,8-11.303,8c-6.627,0-12-5.373-12-12c0-6.627,5.373-12,12-12c3.059,0,5.842,1.154,7.961,3.039l5.657-5.657C34.046,6.053,29.268,4,24,4C12.955,4,4,12.955,4,24c0,11.045,8.955,20,20,20c11.045,0,20-8.955,20-20C44,22.659,43.862,21.35,43.611,20.083z"
              />
              <path
                fill="#FF3D00"
                d="M6.306,14.691l6.571,4.819C14.655,15.108,18.961,12,24,12c3.059,0,5.842,1.154,7.961,3.039l5.657-5.657C34.046,6.053,29.268,4,24,4C16.318,4,9.656,8.337,6.306,14.691z"
              />
              <path
                fill="#4CAF50"
                d="M24,44c5.166,0,9.86-1.977,13.409-5.192l-6.19-5.238C29.211,35.091,26.715,36,24,36c-5.202,0-9.619-3.317-11.283-7.946l-6.522,5.025C9.505,39.556,16.227,44,24,44z"
              />
              <path
                fill="#1976D2"
                d="M43.611,20.083H42V20H24v8h11.303c-0.792,2.237-2.231,4.166-4.087,5.571c0.001-0.001,0.002-0.001,0.003-0.002l6.19,5.238C36.971,39.205,44,34,44,24C44,22.659,43.862,21.35,43.611,20.083z"
              />
            </svg>
            Sign up with Google
          </button>

          <div className="mt-4 text-sm flex items-center">
            <p className="pl-12 md:mr-0">Already have an account?</p>
            <button
              className="register py-2 px-0.5 font-semibold text-[#8DD3BB] font-bold"
              onClick={() => navigate("/login")}
            >
              Login
            </button>
          </div>
        </div>

        {/* Right Side */}
        <div className="md:block hidden w-1/2">
          <img
            className="rounded-2xl max-h-[1200px] w-[900rem] max-w-full"
            src="https://images.unsplash.com/photo-1550697318-929498858774?fm=jpg&q=60&w=3000&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
            alt="login form"
          />
        </div>
      </div>
    </section>
  );
};

export default SignupPage;
