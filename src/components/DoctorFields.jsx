import React from 'react';

const DoctorFields = ({ register, errors }) => {
  return (
    <div className="space-y-3 mt-4">
      <div>
        <label className="block text-sm font-medium">Qualification</label>
        <input
          type="text"
          {...register('qualification')}
          className="w-full px-3 py-2 border rounded-lg focus:ring focus:ring-blue-200"
        />
        {errors.qualification && <p className="text-red-500 text-xs">{errors.qualification.message}</p>}
      </div>
      <div>
        <label className="block text-sm font-medium">Specialization</label>
        <input
          type="text"
          {...register('specialization')}
          className="w-full px-3 py-2 border rounded-lg focus:ring focus:ring-blue-200"
        />
        {errors.specialization && <p className="text-red-500 text-xs">{errors.specialization.message}</p>}
      </div>
      <div>
        <label className="block text-sm font-medium">Experience (Years)</label>
        <input
          type="number"
          {...register('experience')}
          className="w-full px-3 py-2 border rounded-lg focus:ring focus:ring-blue-200"
        />
        {errors.experience && <p className="text-red-500 text-xs">{errors.experience.message}</p>}
      </div>
    </div>
  );
};

export default DoctorFields;
