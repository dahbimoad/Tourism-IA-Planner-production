import React, { useState } from "react";
import { FaRoute, FaRegMoneyBillAlt, FaRegLightbulb, FaRegSmile, FaHeadset, FaHistory, FaPhone, FaEnvelope, FaFacebook, FaTwitter, FaInstagram, FaMapMarkerAlt, FaRobot } from "react-icons/fa";

const AboutSection = () => {
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    subject: "",
    message: ""
  });


 

  const handleInputChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log("Form submitted:", formData);
  };

  return (
    <div id="contact" className="w-full bg-white">
      <div className=" py-20">
        <div className="container mx-auto px-4">
          <div className="max-w-5xl mx-auto">
            <h2 className="text-4xl font-bold text-center text-gray-800 mb-4">GET IN <span className="text-[#8DD3BB]">TOUCH</span></h2>
            <p className="text-xl text-center text-black mb-12">We're here to help you plan the perfect Moroccan adventure</p>
            
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
              <div className="bg-white p-8 rounded-lg shadow-xl">
                <form onSubmit={handleSubmit} className="space-y-6">
                  <div>
                    <input
                      type="text"
                      name="name"
                      placeholder="Your Name"
                      className="w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-[#8DD3BB] focus:border-transparent"
                      onChange={handleInputChange}
                      required
                    />
                  </div>
                  <div>
                    <input
                      type="email"
                      name="email"
                      placeholder="Your Email"
                      className="w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-[#8DD3BB] focus:border-transparent"
                      onChange={handleInputChange}
                      required
                    />
                  </div>
                  <div>
                    <input
                      type="text"
                      name="subject"
                      placeholder="Subject"
                      className="w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-[#8DD3BB] focus:border-transparent"
                      onChange={handleInputChange}
                      required
                    />
                  </div>
                  <div>
                    <textarea
                      name="message"
                      placeholder="What can we help you with today?"
                      rows="4"
                      className="w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-[#8DD3BB] focus:border-transparent"
                      onChange={handleInputChange}
                      required
                    ></textarea>
                  </div>
                  <button
                    type="submit"
                    className="w-full bg-gradient-to-r from-[#8DD3BB] to-[#5b6763] text-white font-semibold py-3 rounded-lg hover:opacity-90 transition-opacity"
                  >
                    Send Message
                  </button>
                </form>
              </div>

              <div className="space-y-8">
                <div className="bg-white p-8 rounded-lg shadow-xl">
                  <h3 className="text-2xl font-semibold mb-6 text-gray-800">Other Ways to Connect</h3>
                  <div className="space-y-4">
                    <div className="flex items-center text-gray-700">
                      <FaPhone className="text-[#8DD3BB] text-xl mr-4" />
                      <span>+212 6090782232</span>
                    </div>
                    <div className="flex items-center text-gray-700">
                      <FaEnvelope className="text-[#8DD3BB] text-xl mr-4" />
                      <span>contact@smartmoroccotravel.com</span>
                    </div>
                    <div className="flex items-center text-gray-700">
                      <FaMapMarkerAlt className="text-[#8DD3BB] text-xl mr-4" />
                      <span>Tanger, Morocco</span>
                    </div>
                  </div>

                  <div className="mt-8">
                    <h4 className="font-semibold mb-4 text-gray-800">Follow Us</h4>
                    <div className="flex space-x-4">
                      <a href="#" className="text-2xl text-[#8DD3BB] hover:text-blue-600 transition-colors">
                        <FaFacebook />
                      </a>
                      
                      <a href="#" className="text-2xl text-[#8DD3BB] hover:text-red-300 transition-colors">
                        <FaInstagram />
                      </a>
                    </div>
                  </div>
                </div>

                <div className="bg-white p-8 rounded-lg shadow-xl">
                  <div className="flex items-center justify-between mb-4">
                    <h4 className="font-semibold text-gray-800">Need Immediate Help?</h4>
                    <FaRobot className="text-2xl text-[#8DD3BB]" />
                  </div>
                  <button className="w-full bg-gray-100 text-gray-700 font-semibold py-3 rounded-lg hover:bg-gray-200 transition-colors">
                    Chat with Our AI Assistant
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      
    </div>
  );
};

export default AboutSection;