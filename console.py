
#!/usr/bin/python3
"""the console program for AirBnB."""

import cmd
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models import storage
import json
import re

classes = {
    "BaseModel": BaseModel,
    "User": User,
    "State": State,
    "City": City,
    "Amenity": Amenity,
    "Place": Place,
    "Review": Review
}
class HBNBCommand(cmd.Cmd):
    """Defines the command interpreter.

        Attributes:
            prompt (str): The command prompt.
    """
    intro = ""
    prompt = "(hbnb) "

    def do_create(self, args):
        """
        Creates a new instance of BaseModel,
        saves it (to the JSON file) and prints the id
        """
        args_list = args.split()

        if len(args_list) < 1:
            print("** class name missing **")
            return False
        if args_list[0] not in classes.keys():
            print("** class doesn't exist **")
            return False
        else:
            new_instance = classes[args_list[0]]()
            new_instance.save()
            print(new_instance.id)

    def do_show(self, line):
        """Prints the string representation of an instance."""
        if line == "" or line is None:
            print("** class name missing **")
        else:
            words = line.split(' ')
            if words[0] not in classes:
                print("** class doesn't exist **")
            elif len(words) < 2:
                print("** instance id missing **")
            else:
                key = "{}.{}".format(words[0], words[1])
                if key not in storage.all():
                    print("** no instance found **")
                else:
                    print(storage.all()[key])

    def do_destroy(self, args):
        """
         Deletes an instance based on the class name and id
         (save the change into the JSON file)
        """
        args_list = args.split()
        if len(args_list) < 1:
            print("** class name missing **")
            return False
        elif args_list[0] not in classes:
            print("** class doesn't exist **")
            return False
        elif len(args_list) < 2:
            print("** instance id missing **")
            return False
        else:
            objects = storage.all()
            key = "{}.{}".format(args_list[0], args_list[1])
            required_key = objects.get(key, None)
            if required_key is None:
                print("** no instance found ***")
                return
            del objects[key]
            storage.save()

    def do_all(self, args):
        """
        Prints all string representation of all instances based
        or not on the class name
        """
        if args == 'all':
            print(["{}".format(str(instance)) for instance in storage.all().values()])
        elif ' ' in args:
            args_list = args.split()
            class_name = args_list[1]
            if class_name in classes.keys():
                class_obj = classes[class_name]
                instances = class_obj.all()
                print(["{}".format(str(instance)) for instance in instances])
            else:
                print("** Class doesn't exist **")
        elif '.' in args:
            args_list = args.split('.')
            class_name = args_list[0]
            if class_name in classes.keys():
                class_obj = classes[class_name]
                instances = class_obj.all()
                print(["{}".format(str(instance)) for instance in instances])
            else:
                print("** Class doesn't exist **")
        else:
            print("** Invalid command. Use 'all <class name>' to retrieve instances **")

        return

  

     def do_update(self, args):
        """
        update <class name> <id> <attribute name> "<attribute value>"
        """
        args_list = args.split(maxsplit=3)
        if len(args_list) < 1:
            print("** class name missing **")
            return
        if args_list[0] not in classes:
            print("** class doesn't exist **")
            return
        if len(args_list) < 2:
            print("** instance id missing **")
            return
        instance_objs = storage.all()
        key = "{}.{}".format(args_list[0], args_list[1])
        req_instance = instance_objs.get(key, None)
        if req_instance is None:
            print("** no instance found **")
            return

        if len(args_list) < 3:
            print("** attribute name missing **")
            return
        attribute_name = args_list[2]
        if len(args_list) < 4:
            print("** value missing **")
            return
        attribute_value = args_list[3]
        if attribute_name in ["id", "created_at", "updated_at"]:
            return
        try:
            if isinstance(attribute_value, int):
                attribute_value = int(attribute_value)
            elif isinstance(attribute_value, float):
                attribute_value = float(attribute_value)
        except (ValueError, TypeError):
            print("** invalid value type for the attribute **")
            return
        setattr(req_instance, attribute_name, attribute_value)
        storage.save()

    def do_quit(self, args):
        """Quit command to exit the program"""
        return True

    def do_EOF(self, args):
        """Exits the shell when Ctrl+D is pressed"""
        return True

    def emptyline(self):
        """Override default `empty line + return` behaviour.
        """
        pass

    def do_help(self, arg):
        """To get help on a command, type help <topic>.
        """
        return super().do_help(arg)


if __name__ == "__main__":
    HBNBCommand().cmdloop()
