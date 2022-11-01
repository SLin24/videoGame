import sprites
import settings
platforms = []
platforms.append(sprites.Platform(settings.screen, 300, 600, 200))
platforms.append(sprites.Platform(settings.screen, 600, 450, 300))
platforms.append(sprites.Platform(settings.screen, 900, 300, 400))
platforms.append(sprites.Platform(settings.screen, 580, 300, 100))
platforms.append(sprites.EndPlatform(settings.screen, 1200, 400, 200))


# sorting based on height to make sure the loop checks for the ground in the correct order 
platforms = sorted(platforms, key = lambda x: x.y)
platforms.reverse()
