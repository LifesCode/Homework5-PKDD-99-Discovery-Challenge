import sys
import solutions as s


def print_exercises_names():
    content = "Available exercises names:\n" \
              "ch1-ex1    -> clean the database\n" \
              "ch1-ex2    -> define a problem to improve the bank's services\n" \
              "ch1-ex3    -> Show how Machine Learning can be used to solve this problem\n" \
              "ch2-ex1    -> Predict the average amount of money for an account\n" \
              "ch2-ex2-l1 -> Show which clients have credit cards\n" \
              "ch2-ex2-l2 -> Show which clients asked the bank for loans\n" \
              "ch2-ex2-l3 -> Show which clients are minors\n" \
              "ch2-ex2-l4 -> Show, for each sex, the number of clients\n" \
              "ch2-ex2-l5 -> Show the types of credit cards the bank offers\n"
    print(content)


class Prompt_Interaction:
    exercises = {"ch1-ex1": s.ch1_ex1,
                 "ch1-ex2": s.ch1_ex2,
                 "ch1-ex3": s.ch1_ex3,
                 "ch2-ex1": s.ch2_ex1,
                 "ch2-ex2-l1": s.ch2_ex2_l1,
                 "ch2-ex2-l2": s.ch2_ex2_l2,
                 "ch2-ex2-l3": s.ch2_ex2_l3,
                 "ch2-ex2-l4": s.ch2_ex2_l4,
                 "ch2-ex2-l5": s.ch2_ex2_l5,
                 "invalid_name": s.invalid_exercise
                 }  # dictionary of with [key: values] = [commands: their corresponding functions]

    def __init__(self, argv: list):
        self.exercise_type = "Exercise"
        self.action = ""
        self.exercise = None
        if "-h" in argv:
            self.action = "help"
            argv.remove("-h")  # remove the command help from the prompt-given parameters of execution
            if not len(argv):
                self.exercise_type = "function"
                self.exercise = print_exercises_names
                return
        elif "-s" in argv:
            argv.remove("-s")  # remove the command help from the prompt-given parameters of execution
            self.action = "solve"
        for ex in self.exercises:
            if ex in argv:
                self.exercise = self.exercises[ex]()
                break

    def execute(self):
        if self.exercise is None:  # prevents executing non-existing exercises
            self.exercise = self.exercises["invalid_name"]()
            self.exercise.solve()
        elif self.exercise_type == "function":
            self.exercise()
        elif self.action == "help":
            self.exercise.help()
        else:
            self.exercise.solve()


if __name__ == "__main__":
    HW5_main_system = Prompt_Interaction(sys.argv[1:])
    HW5_main_system.execute()
