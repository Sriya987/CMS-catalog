import { useEffect, useState } from "react";
import { apiFetch } from "../api";
import { useParams } from "react-router-dom";

export default function Lesson() {
  const { id } = useParams();
  const [lesson, setLesson] = useState(null);

  useEffect(() => {
    apiFetch(`/catalog/lessons/${id}`).then(setLesson);
  }, [id]);

  if (!lesson) return null;

  return (
    <>
      <h2>{lesson.title}</h2>
      <pre>{JSON.stringify(lesson, null, 2)}</pre>
    </>
  );
}
