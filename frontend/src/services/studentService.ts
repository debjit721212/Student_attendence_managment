import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL;

export const registerStudent = async (
    name: string,
    fatherName: string,
    motherName: string,
    rollNumber: string,
    dob: string,
    gender: string,
    classGrade: string,
    photo: string | null,
    address: string,
    parentMobile: string,
    emergencyContact: string
): Promise<any> => {
    const token = localStorage.getItem('token');
    const response = await axios.post(
        `${API_URL}/students/register`,
        {
            name,
            father_name: fatherName,
            mother_name: motherName,
            roll_number: rollNumber,
            dob,
            gender,
            class_grade: classGrade,
            photo,
            address,
            parent_mobile: parentMobile,
            emergency_contact: emergencyContact
        },
        { headers: { Authorization: `Bearer ${token}` } }
    );
    return response.data;
};