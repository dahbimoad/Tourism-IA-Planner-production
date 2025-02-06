import React, { useState, useContext } from "react";
import { useNavigate } from "react-router-dom";
import { AuthContext } from "../contexts/AuthContext";

const SignupPage = () => {
  const navigate = useNavigate();
  const { signup, isLoading, error: authError } = useContext(AuthContext);

  // États locaux
  const [formData, setFormData] = useState({
    nom: "",
    prenom: "",
    email: "",
    password: "",
    passwordConfirm: "",
  });

  const [formErrors, setFormErrors] = useState({});

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));

    // Effacer l'erreur spécifique si l'utilisateur corrige le champ
    if (formErrors[name]) {
      setFormErrors((prev) => ({
        ...prev,
        [name]: "",
      }));
    }
  };

  const validateForm = () => {
    const errors = {};

    // Validation email
    if (!formData.email) {
      errors.email = "Email est requis";
    } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
      errors.email = "Email invalide";
    }

    // Validation nom et prénom
    if (!formData.nom) errors.nom = "Nom est requis";
    if (!formData.prenom) errors.prenom = "Prénom est requis";

    // Validation password
    if (!formData.password) {
      errors.password = "Mot de passe requis";
    } else if (formData.password.length < 8) {
      errors.password = "Le mot de passe doit avoir au moins 8 caractères";
    }

    // Validation confirmation password
    if (formData.password !== formData.passwordConfirm) {
      errors.passwordConfirm = "Les mots de passe ne correspondent pas";
    }

    setFormErrors(errors);
    return Object.keys(errors).length === 0;
  };

  const handleSignup = async (e) => {
    e.preventDefault();

    if (validateForm()) {
      const { passwordConfirm, ...signupData } = formData; // Supprimer passwordConfirm



      const result = await signup(signupData);

      if (result) {
        navigate("/login"); // Redirection après succès
      }
    }
  };

  return (
    <section className="bg-white-100 min-h-screen flex justify-center items-center">
      <div className="bg-[#ffffff] rounded-2xl flex max-w-3xl p-5 items-center">
        <div className="md:w-1/2 px-8">
          <h2 className="font-bold text-3xl text-[#000000]">Register</h2>
          <p className="text-sm mt-4 text-[#112211]">
            Découvrez votre deuxième pays,{" "}
            <span className="text-red-500 font-bold">MORO</span>
            <span className="text-green-600 font-bold">CCO.</span>
          </p>

          {/* Affichage des erreurs */}
          {(authError || Object.keys(formErrors).length > 0) && (
            <div
              className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative"
              role="alert"
            >
              {authError && <p className="font-bold">{authError}</p>}
              {Object.entries(formErrors).map(
                ([field, error], index) => error && <p key={index}>• {error}</p>
              )}
            </div>
          )}

          <form onSubmit={handleSignup} className="flex flex-col gap-4">
            <input
              className={`p-2 mt-6 rounded border ${
                formErrors.email ? "border-red-500" : ""
              }`}
              type="email"
              name="email"
              placeholder="Votre email"
              value={formData.email}
              onChange={handleChange}
            />

            <input
              className={`p-2 rounded border ${
                formErrors.nom ? "border-red-500" : ""
              }`}
              type="text"
              name="nom"
              placeholder="Votre nom"
              value={formData.nom}
              onChange={handleChange}
            />

            <input
              className={`p-2 rounded border ${
                formErrors.prenom ? "border-red-500" : ""
              }`}
              type="text"
              name="prenom"
              placeholder="Votre prénom"
              value={formData.prenom}
              onChange={handleChange}
            />

            <input
              className={`p-2 rounded border w-full ${
                formErrors.password ? "border-red-500" : ""
              }`}
              type="password"
              name="password"
              placeholder="Mot de passe"
              value={formData.password}
              onChange={handleChange}
            />

            <input
              className={`p-2 rounded border w-full ${
                formErrors.passwordConfirm ? "border-red-500" : ""
              }`}
              type="password"
              name="passwordConfirm"
              placeholder="Confirmer le mot de passe"
              value={formData.passwordConfirm}
              onChange={handleChange}
            />

            <button
              className="bg-[#8DD3BB] text-black py-2 rounded hover:scale-105 duration-300 hover:bg-[#14183E] hover:text-[#FFF1DA] font-medium"
              type="submit"
              disabled={isLoading}
            >
              {isLoading ? "Inscription en cours..." : "S'inscrire"}
            </button>
          </form>

          <div className="mt-4 text-sm flex items-center">
            <p>Déjà un compte ?</p>
            <button
              className="register py-2 px-0.5 font-semibold text-[#8DD3BB] font-bold"
              onClick={() => navigate("/login")}
            >
              Connexion
            </button>
          </div>
        </div>

        <div className="md:block hidden w-1/2">
          <img
            className="rounded-2xl max-h-[1200px] w-[900rem] max-w-full"
            src="https://images.unsplash.com/photo-1550697318-929498858774?fm=jpg&q=60&w=3000&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
            alt="Formulaire d'inscription"
          />
        </div>
      </div>
    </section>
  );
};

export default SignupPage;
