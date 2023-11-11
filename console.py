#!/usr/bin/python3
"""Defines the HBnB console."""
import cmd
import re
from shlex import split
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


def parse_1(arg):
    curly_braces = re.search(r"\{(.*?)\}", arg)
    brackets = re.search(r"\[(.*?)\]", arg)
    if curly_braces is None:
        if brackets is None:
            return [i.strip(",") for i in split(arg)]
        else:
            lexer = split(arg[:brackets.span()[0]])
            retl = [i.strip(",") for i in lexer]
            retl.append(brackets.group())
            return retl
    else:
        lexer = split(arg[:curly_braces.span()[0]])
        retl = [i.strip(",") for i in lexer]
        retl.append(curly_braces.group())
        return retl


class HBNBCommand(cmd.Cmd):
    """Defines the BnB command interpreter.

    Attributes:
        prompt (string): The command prompt.
    """

    prompt = "(hbnb) "
    __classes = {
        "BaseModel",
        "User",
        "State",
        "City",
        "Place",
        "Amenity",
        "Review"
    }

    def emptyline(self):
        """Do nothing upon receiving an empty line."""
        pass

    def default(self, arg):
        """Default behavior for cmd module when input is invalid"""
        argdict = {
            "all": self.do_all,
            "show": self.do_show,
            "destroy": self.do_destr,
            "count": self.do_counter,
            "update": self.do_updater
        }
        match = re.search(r"\.", arg)
        if match is not None:
            argl_2 = [arg[:match.span()[0]], arg[match.span()[1]:]]
            match = re.search(r"\((.*?)\)", argl_2[1])
            if match is not None:
                command = [argl_2[1][:match.span()[0]], match.group()[1:-1]]
                if command[0] in argdict.keys():
                    call = "{} {}".format(argl_2[0], command[1])
                    return argdict[command[0]](call)
        print("*** Unknown syntax: {}".format(arg))
        return False

    def do_quit(self, arg):
        """Quit command to exit the program."""
        return True

    def do_EOF(self, arg):
        """EOF signal to exit the program."""
        print("")
        return True

    def do_create(self, arg):
        """Usage: create <class>
        Create a new class instance and print its id.
        """
        argl_2 = parse_1(arg)
        if len(argl_2) == 0:
            print("** class name missing **")
        elif argl_2[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            print(eval(argl_2[0])().id)
            storage.save()

    def do_show(self, arg):
        """Usage: show <class> <id> or <class>.show(<id>)
        Display the string representation of a class instance of a given id.
        """
        argl_2 = parse_1(arg)
        objdict = storage.all()
        if len(argl_2) == 0:
            print("** class name missing **")
        elif argl_2[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(argl_2) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(argl_2[0], argl_2[1]) not in objdict:
            print("** no instance found **")
        else:
            print(objdict["{}.{}".format(argl_2[0], argl_2[1])])

    def do_destr(self, arg):
        """Usage: destroy <class> <id> or <class>.destroy(<id>)
        Delete a class instance of a given id."""
        argl_2 = parse_1(arg)
        objdict = storage.all()
        if len(argl_2) == 0:
            print("** class name missing **")
        elif argl_2[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(argl_2) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(argl_2[0], argl_2[1]) not in objdict.keys():
            print("** no instance found **")
        else:
            del objdict["{}.{}".format(argl_2[0], argl_2[1])]
            storage.save()

    def do_all(self, arg):
        """Usage: all or all <class> or <class>.all()
        Display string representations of all instances of a given class.
        If no class is specified, displays all instantiated objects."""
        argl_2 = parse_1(arg)
        if len(argl_2) > 0 and argl_2[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            objl = []
            for obj in storage.all().values():
                if len(argl_2) > 0 and argl_2[0] == obj.__class__.__name__:
                    objl.append(obj.__str__())
                elif len(argl_2) == 0:
                    objl.append(obj.__str__())
            print(objl)

    def do_counter(self, arg):
        """Usage: count <class> or <class>.count()
        Retrieve the number of instances of a given class."""
        argl_2 = parse_1(arg)
        count = 0
        for obj in storage.all().values():
            if argl_2[0] == obj.__class__.__name__:
                count += 1
        print(count)

    def do_updater(self, arg):
        """Usage: update <class> <id> <attribute_name> <attribute_value> or
       <class>.update(<id>, <attribute_name>, <attribute_value>) or
       <class>.update(<id>, <dictionary>)
        Update a class instance of a given id by adding or updating
        a given attribute key/value pair or dictionary."""
        argl_2 = parse_1(arg)
        objdict = storage.all()

        if len(argl_2) == 0:
            print("** class name missing **")
            return False
        if argl_2[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return False
        if len(argl_2) == 1:
            print("** instance id missing **")
            return False
        if "{}.{}".format(argl_2[0], argl_2[1]) not in objdict.keys():
            print("** no instance found **")
            return False
        if len(argl_2) == 2:
            print("** attribute name missing **")
            return False
        if len(argl_2) == 3:
            try:
                type(eval(argl_2[2])) != dict
            except NameError:
                print("** value missing **")
                return False

        if len(argl_2) == 4:
            obj = objdict["{}.{}".format(argl_2[0], argl_2[1])]
            if argl_2[2] in obj.__class__.__dict__.keys():
                valtype = type(obj.__class__.__dict__[argl_2[2]])
                obj.__dict__[argl_2[2]] = valtype(argl_2[3])
            else:
                obj.__dict__[argl_2[2]] = argl_2[3]
        elif type(eval(argl_2[2])) == dict:
            obj = objdict["{}.{}".format(argl_2[0], argl_2[1])]
            for k, v in eval(argl_2[2]).items():
                if (k in obj.__class__.__dict__.keys() and
                        type(obj.__class__.__dict__[k]) in {str, int, float}):
                    valtype = type(obj.__class__.__dict__[k])
                    obj.__dict__[k] = valtype(v)
                else:
                    obj.__dict__[k] = v
        storage.save()


if __name__ == "__main__":
    HBNBCommand().cmdloop()
