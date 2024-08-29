#!/usr/bin/env python3
import cmd
from models.base_model import BaseModel
from models.user import User
from models.artwork import ArtWork
from models.review import Review
from models.order import Order
from models import storage

class AfriArts(cmd.Cmd):
    """Command interpreter for Afri-Arts Gallery Showcase."""
    
    prompt = "(afri) "
    classes = {
        "BaseModel": BaseModel,
        "User": User,
        "ArtWork": ArtWork,
        "Review": Review,
        "Order": Order
    }
    
    def do_create(self, class_name):
        """Create a new instance of BaseModel, save it, and print the id."""
        if not class_name:
            print("** class name missing **")
        elif class_name not in self.classes:
            print("** class doesn't exist **")
        else:
            new_instance = self.classes[class_name]()
            new_instance.save()
            print(new_instance.id)

    def do_show(self, arg):
        """Prints the string representation of an instance based on the class name and id."""
        # Check if the command is in the format <class name>.show(<id>)
        if '.' in arg and 'show' in arg:
            try:
                class_name, method_call = arg.split('.', 1)
                method, id_call = method_call.split('(', 1)
                instance_id = id_call.rstrip(')')
                instance_id = instance_id.strip('"')  # Remove quotes if present
                print(instance_id)
                if method.strip() != "show":
                    raise ValueError
                args = [class_name, instance_id]
            except ValueError:
                print("** invalid command format **")
                return
        else:
            args = arg.split()
    
        if not args:
            print("** class name missing **")
            return
        if args[0] not in self.classes:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
    
        key = f"{args[0]}.{args[1]}"
        if key not in storage.all():
            print("** no instance found **")
            return
    
        print(storage.all()[key])
    

    def do_destroy(self, args):
        """Delete an instance based on class name and id."""
        args = args.split()
        if not args:
            print("** class name missing **")
        elif args[0] not in self.classes:
            print("** class doesn't exist **")
        elif len(args) < 2:
            print("** instance id missing **")
        else:
            key = f"{args[0]}.{args[1]}"
            if key not in storage.all():
                print("** no instance found **")
            else:
                del storage.all()[key]
                storage.save()

    def do_all(self, class_name):
        """Print all string representations of all instances."""
        if class_name and class_name not in self.classes:
            print("** class doesn't exist **")
        else:
            obj_list = []
            for key, obj in storage.all().items():
                if not class_name or key.startswith(class_name):
                    obj_list.append(str(obj))
            print(obj_list)

    def do_update(self, args):
        """Update an instance based on class name and id."""
        args = args.split()
        if not args:
            print("** class name missing **")
        elif args[0] not in self.classes:
            print("** class doesn't exist **")
        elif len(args) < 2:
            print("** instance id missing **")
        elif len(args) < 3:
            print("** attribute name missing **")
        elif len(args) < 4:
            print("** value missing **")
        else:
            key = f"{args[0]}.{args[1]}"
            obj = storage.all().get(key)
            if not obj:
                print("** no instance found **")
            else:
                attr_name = args[2]
                attr_value = args[3].strip('"')

                # Cast attribute to correct type
                if hasattr(obj, attr_name):
                    attr_type = type(getattr(obj, attr_name))
                    try:
                        attr_value = attr_type(attr_value)
                    except ValueError:
                        print("** value type mismatch **")
                        return

                setattr(obj, attr_name, attr_value)
                obj.save()

    def emptyline(self):
        """Override the default behavior to do nothing on an empty line."""
        pass

    def do_quit(self, arg):
        """Exit the command interpreter."""
        return True

if __name__ == '__main__':
    AfriArts().cmdloop()
