#define CATCH_CONFIG_MAIN
#include <catch2/catch_test_macros.hpp>
#include <SFML/Window.hpp>
#include <iostream>
#include <cmath>

bool isPair(unsigned int number)
{
    return number % 2 == 0;
}

//TEST_CASE("Tests", "Basique")
//{
//    CHECK(isPair(0));
//    CHECK(isPair(2));
//    CHECK(isPair(6));
//    CHECK(isPair(8));
//    CHECK(isPair(16));
//}

SCENARIO("Il etait une fois, une puissance.", "[x^n]")
{
    GIVEN("Parmis ces puissances :")
    {
        int n = 0;

        REQUIRE(n >= 0);

        WHEN("On augmente la puissance")
        {
            n += 2;
            THEN("La puissance est plus grande ?")
            {
                REQUIRE(n < 2);
            }
        }
    }
}

//int main()
//{
//    sf::Window window(sf::VideoMode({ 800,600 }), "SFML");
//    window.setTitle("VCPKG-SFMl");
//
//    while (window.isOpen())
//    {
//        while (const std::optional event = window.pollEvent())
//        {
//            if (event->is<sf::Event::Closed>())
//            {
//                window.close();
//            }
//        }
//        window.display();
//    }
//
//    return 0;
//}
