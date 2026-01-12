import { useParams } from "react-router-dom";
import { useEffect, useState } from "react";
import api from "../api";

export default function ProgramDetail() {
  const { id } = useParams();
  const [program, setProgram] = useState(null);

  useEffect(() => {
    api.get(`/catalog/programs/${id}`).then(setProgram);
  }, [id]);

  if (!program) return <div className="container">Loading...</div>;

  return (
    <div className="container">
      <h2>{program.title}</h2>
      <p>{program.description}</p>

      {program.terms.map(term => (
        <div className="card" key={term.id}>
          <h4>Term {term.term_number}</h4>
          <ul>
            {term.lessons.map(lesson => (
              <li key={lesson.id}>{lesson.lesson_number}. {lesson.title}</li>
            ))}
          </ul>
        </div>
      ))}
    </div>
  );
}
