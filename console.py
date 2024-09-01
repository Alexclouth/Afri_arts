#!/usr/bin/env python3
import cmd
from models.base_model import BaseModel
from models.user import User
from models.artist import Artist
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

    def emptyline(self):
        """Override the default behavior to do nothing on an empty line."""
        pass

    def do_quit(self, arg):
        """Exit the command interpreter."""
        return True
    
    def do_create(self, args):
        """ Create an object of any class"""
        if not args:
            print("** class name missing **")
            return
        arg_list = args.split()
        class_name = arg_list[0]
        if class_name not in self.classes:
            print("** class doesn't exist **")
            return

        new_instance = self.classes[class_name]()

        for arg in arg_list[1:]:
            param = arg.split('=')
            key = param[0]
            val = param[1]

            if val[0] == '\"':
                val = val.replace('\"', '').replace('_', ' ')
            elif '.' in val:
                val = float(val)
            else:
                val = int(val)

            setattr(new_instance, key, val)

        new_instance.save()
        print(new_instance.id)

    def do_show(self, arg):
        """Prints the string representation of an instance based on the class name and id."""
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
                try:
                    attr_value = eval(attr_value)
                except Exception as e:
                    pass

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

    def do_count(self, class_name):
        """Counts the number of instances of a given class."""
        if class_name not in self.classes:
            print("** class doesn't exist **")
            return

        count = sum(1 for obj in storage.all().values() if obj.__class__.__name__ == class_name)
        print(count)
        
    def default(self, line):
        """Handle custom command syntax like <class name>.show(<id>)"""
        if '.' in line and '(' in line and ')' in line:
            try:
                class_name, method_call = line.split('.', 1)
                method, args = method_call.split('(', 1)
                args = args.rstrip(')').strip('"')
                
                if method == "show":
                    self.do_show(f"{class_name} {args}")
                elif method == "all":
                    self.do_all(f"{class_name}")
                elif method == "count":
                    self.do_count(class_name)
                elif method == "destroy":
                    self.do_destroy(f"{class_name} {args}")
                elif method == "update":
                    args = args.split(', ', 1)
                    try:
                        args[1] = eval(args[1])
                    except Exception as e:
                        pass
                    if isinstance(args[1], dict):
                        instance_id = args[0].strip().strip('"')
                        for key, value in args[1].items():
                            self.do_update(f"{class_name} {instance_id} {key} {value}")
                    else:
                        instance_id = args[0].strip().strip('"')
                        args1 = args[1].split(',', 1)
                        attribute_name = args1[0].strip().strip('"')
                        attribute_value = args1[1].strip().strip('"')
                        self.do_update(f"{class_name} {instance_id} {attribute_name} {attribute_value}")
                else:
                    print(f"*** Unknown syntax: {line}")
            except Exception as e:
                print(f"*** Unknown syntax: {line}")
        else:
            print(f"*** Unknown syntax: {line}")

    

if __name__ == '__main__':
    AfriArts().cmdloop()
