import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import { motion, AnimatePresence } from 'framer-motion';
import { useAuth } from '../contexts/AuthContext';
import DoctorFields from './DoctorFields';
import Lottie from 'lottie-react';
import healthcareAnimation from '../assets/healthcare.json';

const AuthForm = () => {
  const [isLogin, setIsLogin] = useState(true);
  const [loading, setLoading] = useState(false);
  const [role, setRole] = useState('patient');
  const { login, registerUser } = useAuth();

  const { register, handleSubmit, formState: { errors } } = useForm();

  const onSubmit = async (data) => {
    setLoading(true);
    if (isLogin) {
      await login(data);
    } else {
      await registerUser(data);
    }
    setLoading(false);
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-gradient-to-br from-blue-50 to-blue-100">
      <div className="flex bg-white shadow-xl rounded-2xl overflow-hidden max-w-4xl w-full">
        
        {/* Left Lottie Animation */}
        <div className="w-1/2 bg-blue-50 flex items-center justify-center p-6">
          <Lottie animationData={healthcareAnimation} loop={true} />
        </div>

        {/* Right Auth Form */}
        <div className="w-1/2 p-8">
          <h2 className="text-2xl font-bold text-center mb-6">{isLogin ? 'Login' : 'Create Account'}</h2>

          <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
            {!isLogin && (
              <div>
                <label className="block text-sm font-medium">Full Name</label>
                <input
                  type="text"
                  {...register('full_name', { required: !isLogin })}
                  className="w-full px-3 py-2 border rounded-lg focus:ring focus:ring-blue-200"
                />
                {errors.full_name && <p className="text-red-500 text-xs">Full name is required</p>}
              </div>
            )}

            <div>
              <label className="block text-sm font-medium">Email</label>
              <input
                type="email"
                {...register('email', { required: true })}
                className="w-full px-3 py-2 border rounded-lg focus:ring focus:ring-blue-200"
              />
              {errors.email && <p className="text-red-500 text-xs">Email is required</p>}
            </div>

            <div>
              <label className="block text-sm font-medium">Password</label>
              <input
                type="password"
                {...register('password', { required: true })}
                className="w-full px-3 py-2 border rounded-lg focus:ring focus:ring-blue-200"
              />
              {errors.password && <p className="text-red-500 text-xs">Password is required</p>}
            </div>

            {!isLogin && (
              <>
                <div>
                  <label className="block text-sm font-medium">Role</label>
                  <select
                    {...register('role')}
                    className="w-full px-3 py-2 border rounded-lg focus:ring focus:ring-blue-200"
                    onChange={(e) => setRole(e.target.value)}
                  >
                    <option value="patient">Patient</option>
                    <option value="doctor">Doctor</option>
                  </select>
                </div>

                <AnimatePresence>
                  {role === 'doctor' && (
                    <motion.div
                      initial={{ opacity: 0, height: 0 }}
                      animate={{ opacity: 1, height: 'auto' }}
                      exit={{ opacity: 0, height: 0 }}
                      transition={{ duration: 0.4 }}
                    >
                      <DoctorFields register={register} errors={errors} />
                    </motion.div>
                  )}
                </AnimatePresence>
              </>
            )}

            <button
              type="submit"
              disabled={loading}
              className="w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 transition"
            >
              {loading ? 'Please wait...' : isLogin ? 'Login' : 'Register'}
            </button>
          </form>

          <p className="text-center text-sm mt-4">
            {isLogin ? "Don't have an account?" : "Already have an account?"}{' '}
            <button
              onClick={() => setIsLogin(!isLogin)}
              className="text-blue-600 font-semibold hover:underline"
            >
              {isLogin ? 'Sign Up' : 'Login'}
            </button>
          </p>
        </div>
      </div>
    </div>
  );
};

export default AuthForm;
