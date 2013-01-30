
from sage.categories.realizations import Category_realization_of_parent
from sage.structure.element import Element
from sage.misc.bindable_class import BindableClass
from sage.structure.parent import Parent
from sage.structure.unique_representation import UniqueRepresentation
from sage.structure.element_wrapper import ElementWrapper
from sage.categories.rings import Rings
from sage.categories.sets_cat import Sets
from sage.categories.homset import Hom
from sage.rings.integer import Integer


class RingOfIntegers(Parent, UniqueRepresentation):
    r"""
    An example of parent endowed with several realizations.
    
    The RingOfIntegers, redone (much slower of course, but to test the idea on a simple case before constructing more complicated parents). 
    
    EXAMPLES::

        sage: A = RingOfIntegers(); A
        Integer Ring (redone)
        
    Two notations of ``A``:

        sage: SageIntegers = A.SageIntegers(); SageIntegers
        Integer Ring (redone) in the realization SageIntegers
        
        sage: LongIntegers = A.LongIntegers(); LongIntegers  
        Integer Ring (redone) in the realization LongIntegers

    Some conversions::

        sage: SageIntegers(LongIntegers("3242"))
        3242
        sage: LongIntegers(SageIntegers(4243))
        '4243'

    We can now mix expressions::

        sage: LongIntegers(SageIntegers(4243)) + LongIntegers("523")   # broken
    """

    def __repr__(self):
        return "Integer Ring (redone)"
        
    def __init__(self):
        r"""
        EXAMPLES::

            sage: A = RingOfIntegers(); A
            Integer Ring (redone)
            sage: TestSuite(A).run()

        TESTS::

            sage: A = Sets().WithRealizations().example(); A
            The subset algebra of {1, 2, 3} over Rational Field
            sage: SageIntegers, LongIntegers = A.realizations()
            sage: type(LongIntegers.coerce_map_from(SageIntegers))
            <type 'sage.categories.morphism.SetMorphism'>
            sage: type(SageIntegers.coerce_map_from(LongIntegers))
            <type 'sage.categories.morphism.SetMorphism'>
            
        """
        Parent.__init__(self, category = Rings().WithRealizations())
        category = self.Notations()
        SageIntegers = self.SageIntegers()
        LongIntegers = self.LongIntegers()
        
        f_Sage_to_Long = lambda self: LongIntegers(str(self))
        Sage_to_Long = \
            Hom(SageIntegers, LongIntegers, Sets().Realizations())(f_Sage_to_Long)
            
        f_Long_to_Sage = lambda self:(SageIntegers(Integer(self.value)))
        Long_to_Sage = \
            Hom(LongIntegers, SageIntegers, Sets().Realizations())(f_Long_to_Sage)

        # Tried:
        # Hom(LongIntegers, SageIntegers, Rings().Realizations())(f_Long_to_Sage)
        # Hom(LongIntegers, SageIntegers, category)(f_Long_to_Sage)
        
        Sage_to_Long.register_as_coercion()
        Long_to_Sage.register_as_coercion()
        
    class Notations(Category_realization_of_parent):
        r"""
        The category of the realizations of the integer ring
        """
        def super_categories(self):
            return [Rings().Realizations()]
            
    class LongIntegers(Parent, UniqueRepresentation, BindableClass):
        r"""
        The integer ring, using strings

        INPUT:

        - ``A`` -- a parent with realization in :class:`RingOfIntegers`

        EXAMPLES::

            sage: A = RingOfIntegers()
            sage: LongIntegers = A.LongIntegers(); LongIntegers
            Integer Ring (redone) in the realization LongIntegers
        """
        def __init__(self, A):
            r"""
            EXAMPLES::
                sage: A = RingOfIntegers()
                sage: LongIntegers = A.LongIntegers(); LongIntegers
                Integer Ring (redone) in the realization LongIntegers
                sage: x = LongIntegers.an_element()
                sage: y = LongIntegers.an_element()
                sage: x
                '7'
                sage: x+y           # broken
            """
            Parent.__init__(self, category = A.Notations())
        def an_element(self):
            return self("7")
        class Element(ElementWrapper):
            wrapped_class = str

    # Because I don't want to change Integer directly, yet want to use the Notations category. There is certainly some better way to do this:
    class SageIntegers(Parent, UniqueRepresentation, BindableClass):
        r"""
        The integer ring, using sage integers

        INPUT:

        - ``A`` -- a parent with realization in :class:`RingOfIntegers`

        EXAMPLES::

            sage: A = RingOfIntegers()
            sage: SageIntegers = A.SageIntegers(); SageIntegers
            Integer Ring (redone) in the realization SageIntegers

        TESTS:

        The product in this basis is computed by converting to the fundamental
        basis, computing the product there, and then converting back::

            sage: A = RingOfIntegers()
            sage: SageIntegers = A.SageIntegers(); SageIntegers
            Integer Ring (redone) in the realization SageIntegers
            sage: x = SageIntegers.an_element()
            sage: y = SageIntegers.an_element()
            sage: SageIntegers.product
            <bound method RingOfIntegers.SageIntegers_with_category.product of Integer Ring (redone) in the realization SageIntegers>            
            sage: x*y
            36
            sage: SageIntegers.product(x, y)
            36
            sage: SageIntegers.summation
            <bound method RingOfIntegers.SageIntegers_with_category.summation of Integer Ring (redone) in the realization SageIntegers>
            sage: x+y
            12
        """
        def product(self, x, y):
            return self(x.value*y.value)
            
        def summation(self, x, y):
            return self(x.value+y.value)

        def __init__(self, A):
            r"""
            EXAMPLES::
                sage: A = RingOfIntegers()
                sage: SageIntegers = A.SageIntegers(); SageIntegers
                Integer Ring (redone) in the realization SageIntegers
                sage: TestSuite(SageIntegers).run()
            """
            Parent.__init__(self, category = A.Notations())
        def an_element(self):
            """
                sage: SageIntegers.an_element()
                6
            """
            return self(Integer(6))
        def one(self):
            return self(Integer(1))
        def zero(self):
            return self(Integer(0))
            
        class Element(ElementWrapper):
            wrapped_class = Integer
            