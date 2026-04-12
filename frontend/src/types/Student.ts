export type Student = {
  studentId: number;
  firstName: string;
  middleName: string | null;
  lastName: string;
  courseId: number;
  courseName: string;
  score: number;
};

export type CreateStudentPayload = {
  studentId: number;
  firstName: string;
  middleName: string | null;
  lastName: string;
  score: number;
  courseId?: number;
};

export type CourseOption = {
  courseId: number;
  courseName: string;
};

export type CourseAverage = {
  courseId: number;
  courseName: string;
  averageScore: number | null;
  enrollmentCount: number;
};

export type CourseAveragesResponse = {
  courseAverages: CourseAverage[];
};

export type DeleteEnrollmentResponse = {
  message: string;
};
