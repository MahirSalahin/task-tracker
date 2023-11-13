import time
import typer
from typing import List

app = typer.Typer()

# tasks[task_name]=[elapsed_time,current_time,is_paused]
tasks = {}

# WHEN A TASK IS DONE
def say_done(task_name: str):
    typer.secho(
        f"---------------------------------------------------------------",
        fg=typer.colors.BRIGHT_GREEN,
    )
    typer.secho(
        f"task: {task_name} is completed successfully...",
        fg=typer.colors.BRIGHT_GREEN,
    )
    show_elapsed_time(task_name)


# UPDATE THE TIMING OF THE TASK
def update_timing(task_name: str):
    if (task_name in tasks) == False:
        typer.secho(
            f"you were not doing any such task called: {task_name}",
            fg=typer.colors.BRIGHT_RED,
        )
        return
    start_time = tasks[task_name][1]
    end_time = time.time()
    tasks[task_name][0] += end_time - start_time
    if tasks[task_name][2] == False:
        tasks[task_name][1] = end_time


# SHOW THE ELAPSED TIME OF A TASK
def show_elapsed_time(task_name: str):
    if tasks[task_name][2] == False:
        update_timing(task_name)
    elapsed_time = tasks[task_name][0]
    mins, secs = divmod(elapsed_time, 60)
    hours, mins = divmod(mins, 60)
    typer.secho(
        f"elapsed time: {hours} hours {mins} mins {round(secs,3)} secs",
        fg=typer.colors.BRIGHT_CYAN,
    )


# GENERATE THE NAME OF THE TASK FROM A LIST[STR]
def generate_task_name(task: List[str]):
    s = "'"
    for word in task:
        s += word + " "
    return s.strip() + "'"


# INTIALIZE TASK
@app.command()
def init(taskname: List[str]):
    # task=typer.prompt("What are you about to do? ")
    task_name = generate_task_name(taskname)
    tasks[task_name] = [0, time.time(), False]
    typer.secho(
        f"task: {task_name} has been initialized",
        fg=typer.colors.GREEN,
    )


# PAUSE
def pause_task(task_name: str):
    if (task_name in tasks) == False:
        typer.secho(
            f"you were not doing any such task: {task_name}", fg=typer.colors.BRIGHT_RED
        )
        return

    if tasks[task_name][2] == True:
        typer.secho(
            f"task: {task_name} was already paused", fg=typer.colors.BRIGHT_RED)
        return

    typer.secho(f"task: {task_name} is paused", fg=typer.colors.BRIGHT_GREEN)
    tasks[task_name][2] = True
    update_timing(task_name)


@app.command()
def pause(taskname: List[str]):
    task_name = generate_task_name(taskname)
    pause_task(task_name)


@app.command()
def pauseall():
    for task in tasks:
        pause_task(task)


# RESUME
def resume_task(task_name: str):
    if (task_name in tasks) == False:
        typer.secho(
            f"you were not doing any such task: {task_name}", fg=typer.colors.BRIGHT_RED
        )
        return

    if tasks[task_name][2] == False:
        typer.secho(f"task: {task_name} was not paused", fg=typer.colors.RED)
        return

    tasks[task_name][1] = time.time()
    tasks[task_name][2] = False
    typer.secho(f"task: {task_name} is resumed", fg=typer.colors.BRIGHT_GREEN)

@app.command()
def resume(taskname: List[str]):
    task_name = generate_task_name(taskname)
    resume_task(task_name)

@app.command()
def resumeall():
    for task in tasks:
        resume_task(task)


# CURRENT TASK'S ELAPSED TIME
def show_task(task_name:str):
        if task_name in tasks == False:
            typer.secho(
            f"you were not doing any such task: {task_name}",
            fg=typer.colors.BRIGHT_RED,
            )
            return
        typer.secho(
            f"---------------------------------------------------------------",
            fg=typer.colors.BRIGHT_GREEN,
        )
        typer.secho(f"task: {task_name}", fg=typer.colors.BRIGHT_GREEN)
        show_elapsed_time(task_name)

@app.command()
def show(task:List[str]):
    task_name=generate_task_name(task)
    show_task(task_name)

@app.command()
def showall():
    if len(tasks) == 0:
        typer.secho(f"currently no task running", fg=typer.colors.BRIGHT_RED)
    for task_name in tasks:
        show_task(task_name)

# TASK DONE
@app.command()
def end(taskname: List[str]):
    task_name = generate_task_name(taskname)
    if task_name in tasks:
        say_done(task_name)
        del tasks[task_name]
    else:
        typer.secho(
            f"you were not doing any such task: {task_name}",
            fg=typer.colors.BRIGHT_RED,
        )

@app.command()
def endall():
    for task_name in tasks:
        say_done(task_name)
    tasks.clear()


# EXIT
@app.command()
def exit():
    typer.secho("goodbye", fg=typer.colors.BRIGHT_MAGENTA)
    raise SystemExit


# MAIN
def main():
    typer.secho("hello :)", fg=typer.colors.BRIGHT_MAGENTA)
    while True:
        command = input().lower()
        if command == "exit":
            exit()

        try:
            app(command.split())
        except SystemExit:
            pass


if __name__ == "__main__":
    main()
    