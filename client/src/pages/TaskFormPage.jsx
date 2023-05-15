import { useEffect } from 'react';
import { useForm } from 'react-hook-form'
import { createTask, deleteTask, updateTask, getTask } from '../api/tasks.api'
import { useNavigate, useParams } from 'react-router-dom';
import { toast } from 'react-hot-toast';

export function TaskFormPage() {

    const {
        register,
        handleSubmit,
        formState: { errors },
        setValue
    } = useForm()
    const navigate = useNavigate();
    const params = useParams()
    console.log(params)

    const onSubmit = handleSubmit(async (data) => {
        if (params.id) {
            await updateTask(params.id, data)
            toast.success('Tarea Actualizada', {
                position: "bottom-right",
                style: {
                    background: "#101010",
                    color: "#fff"
                }
            })

        } else {
            await createTask(data);
            toast.success('Tarea Creada', {
                position: "bottom-right",
                style: {
                    background: "#101010",
                    color: "#fff"
                }
            })
        }
        navigate("/tasks")
    });

    useEffect(() => {
        async function loadTask() {
            if (params.id) {
                const res = await getTask(params.id);
                setValue('title', res.data.title)
                setValue('description', res.data.description)
            }
        }
        loadTask();
    }, []);

    return (
        <div className='max-w-xl mx-auto'>

            <form onSubmit={onSubmit}>
                <input type="text" placeholder="title"
                    {...register("title", { required: true })}
                    className='bg-zinc-700 p-3 rounded-lg block w-full mb-3'
                />

                {errors.title && <span> this field is required </span>}

                <textarea rows="3" placeholder="Description"
                    {...register("description", { required: true })}
                    className='bg-zinc-700 p-3 rounded-lg block w-full mb-3'
                ></textarea>

                {errors.Description && <span> this field is required </span>}

                <button
                    className='bg-indigo-500 p-3 rounded-lg block w-full mt-3'
                >Save</button>
            </form>

            {params.id && (
                <div className='flex justify-end'>
                    <button
                        className='bg-red-500 p-3 rounded-lg w-48 mt-3'
                        onClick={async () => {
                            const accepted = window.confirm('are you sure?')
                            if (accepted) {
                                await deleteTask(params.id);
                                toast.success('Tarea eliminada', {
                                    position: "bottom-right",
                                    style: {
                                        background: "#101010",
                                        color: "#fff"
                                    }
                                })
                                navigate("/tasks");
                            }
                        }}
                    >
                        Delete
                    </button>
                </div>
            )}
        </div>
    );
}